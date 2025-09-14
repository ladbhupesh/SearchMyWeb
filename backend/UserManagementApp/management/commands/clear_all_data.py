import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from UserManagementApp.models import (
    WebsiteLink, 
    SearchQueryLog, 
    WebsiteLinkClick, 
    DailyAnalyticsReports,
    DailyWorldCluodAnalytics,
    StateWiseTrafficAnalytic
)
from UserManagementApp.utils import logger, logger_extra


class Command(BaseCommand):
    help = 'Clear all indexes and pages from database and OpenSearch'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm that you want to delete all data (required for safety)'
        )
        parser.add_argument(
            '--keep-users',
            action='store_true',
            help='Keep user accounts and only clear search data'
        )
        parser.add_argument(
            '--keep-analytics',
            action='store_true',
            help='Keep analytics data and only clear website links and indexes'
        )
        parser.add_argument(
            '--opensearch-only',
            action='store_true',
            help='Only clear OpenSearch indexes, keep database data'
        )
        parser.add_argument(
            '--database-only',
            action='store_true',
            help='Only clear database data, keep OpenSearch indexes'
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.ERROR(
                    'This command will delete ALL data! Use --confirm to proceed.\n'
                    'Available options:\n'
                    '  --keep-users: Keep user accounts\n'
                    '  --keep-analytics: Keep analytics data\n'
                    '  --opensearch-only: Only clear OpenSearch\n'
                    '  --database-only: Only clear database\n'
                )
            )
            return

        self.stdout.write(
            self.style.WARNING('Starting data cleanup process...')
        )

        try:
            # Clear OpenSearch indexes
            if not options['database_only']:
                self.clear_opensearch_indexes()

            # Clear database data
            if not options['opensearch_only']:
                self.clear_database_data(
                    keep_users=options['keep_users'],
                    keep_analytics=options['keep_analytics']
                )

            # Clear file system data
            if not options['opensearch_only']:
                self.clear_file_system_data()

            self.stdout.write(
                self.style.SUCCESS('Data cleanup completed successfully!')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error during cleanup: {str(e)}')
            )
            logger.error(f'Data cleanup error: {str(e)}', extra=logger_extra)

    def clear_opensearch_indexes(self):
        """Clear all OpenSearch indexes"""
        try:
            self.stdout.write('Clearing OpenSearch indexes...')
            
            # Get all indices
            indices = settings.ELASTIC_SEARCH_OBJ.cat.indices(format='json')
            
            if not indices:
                self.stdout.write('No OpenSearch indices found.')
                return

            # Delete all indices
            for index_info in indices:
                index_name = index_info['index']
                if not index_name.startswith('.'):  # Skip system indices
                    try:
                        settings.ELASTIC_SEARCH_OBJ.indices.delete(index=index_name)
                        self.stdout.write(f'Deleted index: {index_name}')
                    except Exception as e:
                        self.stdout.write(
                            self.style.WARNING(f'Could not delete index {index_name}: {str(e)}')
                        )

            # Refresh to ensure changes are applied
            settings.ELASTIC_SEARCH_OBJ.indices.refresh()
            
            self.stdout.write(
                self.style.SUCCESS('OpenSearch indexes cleared successfully!')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error clearing OpenSearch: {str(e)}')
            )
            logger.error(f'OpenSearch cleanup error: {str(e)}', extra=logger_extra)

    def clear_database_data(self, keep_users=False, keep_analytics=False):
        """Clear database data based on options"""
        try:
            self.stdout.write('Clearing database data...')
            
            with transaction.atomic():
                # Clear website links and related data
                website_count = WebsiteLink.objects.count()
                WebsiteLink.objects.all().delete()
                self.stdout.write(f'Deleted {website_count} website links')

                # Clear search query logs
                search_logs_count = SearchQueryLog.objects.count()
                SearchQueryLog.objects.all().delete()
                self.stdout.write(f'Deleted {search_logs_count} search query logs')

                # Clear website link clicks
                clicks_count = WebsiteLinkClick.objects.count()
                WebsiteLinkClick.objects.all().delete()
                self.stdout.write(f'Deleted {clicks_count} website link clicks')

                # Clear analytics data if not keeping it
                if not keep_analytics:
                    analytics_count = DailyAnalyticsReports.objects.count()
                    DailyAnalyticsReports.objects.all().delete()
                    self.stdout.write(f'Deleted {analytics_count} daily analytics reports')

                    wordcloud_count = DailyWorldCluodAnalytics.objects.count()
                    DailyWorldCluodAnalytics.objects.all().delete()
                    self.stdout.write(f'Deleted {wordcloud_count} wordcloud analytics')

                    traffic_count = StateWiseTrafficAnalytic.objects.count()
                    StateWiseTrafficAnalytic.objects.all().delete()
                    self.stdout.write(f'Deleted {traffic_count} state-wise traffic analytics')

                # Clear users if not keeping them
                if not keep_users:
                    from UserManagementApp.models import User
                    user_count = User.objects.count()
                    User.objects.all().delete()
                    self.stdout.write(f'Deleted {user_count} users')

            self.stdout.write(
                self.style.SUCCESS('Database data cleared successfully!')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error clearing database: {str(e)}')
            )
            logger.error(f'Database cleanup error: {str(e)}', extra=logger_extra)

    def clear_file_system_data(self):
        """Clear file system data (indexed files, logs, etc.)"""
        try:
            self.stdout.write('Clearing file system data...')
            
            # Clear indexed data files
            files_dir = os.path.join(settings.BASE_DIR, 'files')
            if os.path.exists(files_dir):
                shutil.rmtree(files_dir)
                os.makedirs(files_dir, exist_ok=True)
                self.stdout.write('Cleared indexed data files')

            # Clear log files (optional - keep recent logs)
            log_dir = os.path.join(settings.BASE_DIR, 'log')
            if os.path.exists(log_dir):
                for file in os.listdir(log_dir):
                    if file.endswith('.log'):
                        file_path = os.path.join(log_dir, file)
                        # Keep last 100 lines of logs
                        with open(file_path, 'r') as f:
                            lines = f.readlines()
                        with open(file_path, 'w') as f:
                            f.writelines(lines[-100:])
                self.stdout.write('Cleared old log entries')

            # Clear reports directory
            reports_dir = os.path.join(settings.BASE_DIR, 'reports')
            if os.path.exists(reports_dir):
                for file in os.listdir(reports_dir):
                    if file.endswith(('.xml', '.report')):
                        os.remove(os.path.join(reports_dir, file))
                self.stdout.write('Cleared report files')

            self.stdout.write(
                self.style.SUCCESS('File system data cleared successfully!')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error clearing file system: {str(e)}')
            )
            logger.error(f'File system cleanup error: {str(e)}', extra=logger_extra)

    def get_data_summary(self):
        """Get summary of current data"""
        try:
            summary = {
                'website_links': WebsiteLink.objects.count(),
                'search_logs': SearchQueryLog.objects.count(),
                'clicks': WebsiteLinkClick.objects.count(),
                'analytics': DailyAnalyticsReports.objects.count(),
                'wordcloud': DailyWorldCluodAnalytics.objects.count(),
                'traffic': StateWiseTrafficAnalytic.objects.count(),
            }
            
            # Get OpenSearch indices
            try:
                indices = settings.ELASTIC_SEARCH_OBJ.cat.indices(format='json')
                summary['opensearch_indices'] = len([i for i in indices if not i['index'].startswith('.')])
            except:
                summary['opensearch_indices'] = 0
            
            return summary
        except Exception as e:
            logger.error(f'Error getting data summary: {str(e)}', extra=logger_extra)
            return {}
