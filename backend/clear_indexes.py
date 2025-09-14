#!/usr/bin/env python3
"""
Script to clear all indexes and pages from database and OpenSearch
Run this from the backend directory: python clear_indexes.py
"""

import os
import sys
import django

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MySearchEngine.settings')
django.setup()

from django.conf import settings
from UserManagementApp.models import WebsiteLink, SearchQueryLog, WebsiteLinkClick
from UserManagementApp.utils import logger, logger_extra


def clear_opensearch_indexes():
    """Clear all OpenSearch indexes"""
    print("🗑️  Clearing OpenSearch indexes...")
    
    try:
        # Get all indices
        indices = settings.ELASTIC_SEARCH_OBJ.cat.indices(format='json')
        
        if not indices:
            print("ℹ️  No OpenSearch indices found.")
            return

        deleted_count = 0
        for index_info in indices:
            index_name = index_info['index']
            if not index_name.startswith('.'):  # Skip system indices
                try:
                    settings.ELASTIC_SEARCH_OBJ.indices.delete(index=index_name)
                    print(f"✅ Deleted index: {index_name}")
                    deleted_count += 1
                except Exception as e:
                    print(f"⚠️  Could not delete index {index_name}: {str(e)}")

        # Refresh to ensure changes are applied
        settings.ELASTIC_SEARCH_OBJ.indices.refresh()
        
        print(f"✅ OpenSearch cleanup complete! Deleted {deleted_count} indices.")

    except Exception as e:
        print(f"❌ Error clearing OpenSearch: {str(e)}")
        logger.error(f'OpenSearch cleanup error: {str(e)}', extra=logger_extra)


def clear_database_data():
    """Clear website links and search data from database"""
    print("🗑️  Clearing database data...")
    
    try:
        # Clear website links
        website_count = WebsiteLink.objects.count()
        WebsiteLink.objects.all().delete()
        print(f"✅ Deleted {website_count} website links")

        # Clear search query logs
        search_logs_count = SearchQueryLog.objects.count()
        SearchQueryLog.objects.all().delete()
        print(f"✅ Deleted {search_logs_count} search query logs")

        # Clear website link clicks
        clicks_count = WebsiteLinkClick.objects.count()
        WebsiteLinkClick.objects.all().delete()
        print(f"✅ Deleted {clicks_count} website link clicks")

        print("✅ Database cleanup complete!")

    except Exception as e:
        print(f"❌ Error clearing database: {str(e)}")
        logger.error(f'Database cleanup error: {str(e)}', extra=logger_extra)


def clear_file_system_data():
    """Clear indexed files and temporary data"""
    print("🗑️  Clearing file system data...")
    
    try:
        import shutil
        
        # Clear indexed data files
        files_dir = os.path.join(settings.BASE_DIR, 'files')
        if os.path.exists(files_dir):
            shutil.rmtree(files_dir)
            os.makedirs(files_dir, exist_ok=True)
            print("✅ Cleared indexed data files")

        # Clear old log entries (keep last 50 lines)
        log_dir = os.path.join(settings.BASE_DIR, 'log')
        if os.path.exists(log_dir):
            for file in os.listdir(log_dir):
                if file.endswith('.log'):
                    file_path = os.path.join(log_dir, file)
                    try:
                        with open(file_path, 'r') as f:
                            lines = f.readlines()
                        with open(file_path, 'w') as f:
                            f.writelines(lines[-50:])
                    except:
                        pass
            print("✅ Cleared old log entries")

        print("✅ File system cleanup complete!")

    except Exception as e:
        print(f"❌ Error clearing file system: {str(e)}")
        logger.error(f'File system cleanup error: {str(e)}', extra=logger_extra)


def get_data_summary():
    """Get summary of current data"""
    print("📊 Current data summary:")
    
    try:
        website_links = WebsiteLink.objects.count()
        search_logs = SearchQueryLog.objects.count()
        clicks = WebsiteLinkClick.objects.count()
        
        print(f"  • Website Links: {website_links}")
        print(f"  • Search Logs: {search_logs}")
        print(f"  • Link Clicks: {clicks}")
        
        # Get OpenSearch indices
        try:
            indices = settings.ELASTIC_SEARCH_OBJ.cat.indices(format='json')
            user_indices = [i for i in indices if not i['index'].startswith('.')]
            print(f"  • OpenSearch Indices: {len(user_indices)}")
            
            if user_indices:
                print("    Indices:")
                for idx in user_indices:
                    print(f"      - {idx['index']} ({idx.get('docs.count', 'N/A')} docs)")
        except Exception as e:
            print(f"  • OpenSearch: Error connecting - {str(e)}")
            
    except Exception as e:
        print(f"❌ Error getting data summary: {str(e)}")


def main():
    """Main function"""
    print("🧹 SearchMyWeb Data Cleanup Script")
    print("=" * 50)
    
    # Show current data
    get_data_summary()
    print()
    
    # Confirm before proceeding
    confirm = input("⚠️  This will delete ALL indexes and pages. Continue? (yes/no): ")
    if confirm.lower() not in ['yes', 'y']:
        print("❌ Operation cancelled.")
        return
    
    print("\n🚀 Starting cleanup process...")
    print()
    
    # Clear OpenSearch indexes
    clear_opensearch_indexes()
    print()
    
    # Clear database data
    clear_database_data()
    print()
    
    # Clear file system data
    clear_file_system_data()
    print()
    
    print("🎉 Cleanup completed successfully!")
    print("\n📊 Final summary:")
    get_data_summary()


if __name__ == "__main__":
    main()
