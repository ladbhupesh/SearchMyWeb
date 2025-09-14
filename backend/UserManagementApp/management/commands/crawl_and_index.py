import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from UserManagementApp.crawl_website import *
from UserManagementApp.models import WebsiteLink, User
from UserManagementApp.utils import crawl_weblink, index_website, logger, logger_extra


class Command(BaseCommand):
    help = 'Crawl and index websites with configurable number of workers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--crawl-workers',
            type=int,
            default=2,
            help='Number of workers for crawling (default: 2)'
        )
        parser.add_argument(
            '--index-workers',
            type=int,
            default=3,
            help='Number of workers for indexing (default: 3)'
        )
        parser.add_argument(
            '--max-crawl-items',
            type=int,
            default=10,
            help='Maximum number of items to crawl in one run (default: 10)'
        )
        parser.add_argument(
            '--max-index-items',
            type=int,
            default=20,
            help='Maximum number of items to index in one run (default: 20)'
        )
        parser.add_argument(
            '--crawl-only',
            action='store_true',
            help='Only perform crawling, skip indexing'
        )
        parser.add_argument(
            '--index-only',
            action='store_true',
            help='Only perform indexing, skip crawling'
        )
        parser.add_argument(
            '--continuous',
            action='store_true',
            help='Run continuously with 10-second intervals'
        )

    def handle(self, *args, **options):
        crawl_workers = options['crawl_workers']
        index_workers = options['index_workers']
        max_crawl_items = options['max_crawl_items']
        max_index_items = options['max_index_items']
        crawl_only = options['crawl_only']
        index_only = options['index_only']
        continuous = options['continuous']

        self.stdout.write(
            self.style.SUCCESS(
                f'Starting simultaneous crawl and index process with {crawl_workers} crawl workers '
                f'and {index_workers} index workers'
            )
        )
        
        if crawl_only and index_only:
            self.stdout.write(self.style.ERROR('Cannot specify both --crawl-only and --index-only'))
            return

        if continuous:
            self.run_continuous(crawl_workers, index_workers, max_crawl_items, max_index_items, crawl_only, index_only)
        else:
            self.run_once(crawl_workers, index_workers, max_crawl_items, max_index_items, crawl_only, index_only)

    def run_continuous(self, crawl_workers, index_workers, max_crawl_items, max_index_items, crawl_only, index_only):
        """Run the process continuously with 10-second intervals"""
        self.stdout.write(self.style.WARNING('Running in continuous mode. Press Ctrl+C to stop.'))
        
        try:
            while True:
                self.run_once(crawl_workers, index_workers, max_crawl_items, max_index_items, crawl_only, index_only)
                time.sleep(10)
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('\nStopped by user.'))

    def run_once(self, crawl_workers, index_workers, max_crawl_items, max_index_items, crawl_only, index_only):
        """Run the crawl and index process once simultaneously"""
        start_time = time.time()
        
        # Create threads for simultaneous execution
        crawl_thread = None
        index_thread = None
        
        # Start crawling thread if not index-only
        if not index_only:
            crawl_thread = threading.Thread(
                target=self.run_crawling,
                args=(crawl_workers, max_crawl_items),
                name='CrawlThread'
            )
            crawl_thread.start()
        
        # Start indexing thread if not crawl-only
        if not crawl_only:
            index_thread = threading.Thread(
                target=self.run_indexing,
                args=(index_workers, max_index_items),
                name='IndexThread'
            )
            index_thread.start()
        
        # Wait for both threads to complete
        if crawl_thread:
            crawl_thread.join()
            self.stdout.write(self.style.SUCCESS('Crawling thread completed'))
        
        if index_thread:
            index_thread.join()
            self.stdout.write(self.style.SUCCESS('Indexing thread completed'))
        
        end_time = time.time()
        self.stdout.write(
            self.style.SUCCESS(
                f'Process completed in {end_time - start_time:.2f} seconds'
            )
        )

    def run_crawling(self, num_workers, max_items):
        """Run crawling with specified number of workers"""
        try:
            logger.info("STARTED crawl_website_scheduler", extra=logger_extra)
            
            # Get items to crawl
            website_links = WebsiteLink.objects.filter(
                is_crawl=True
            ).exclude(
                index_level=None
            )[:max_items]
            
            if not website_links.exists():
                self.stdout.write(self.style.WARNING('No items to crawl.'))
                return
            
            self.stdout.write(f'Crawling {website_links.count()} items with {num_workers} workers...')
            
            # Process with thread pool
            with ThreadPoolExecutor(max_workers=num_workers) as executor:
                futures = []
                
                for website_link_obj in website_links:
                    # Mark as being processed
                    website_link_obj.is_crawl = False
                    website_link_obj.save()
                    
                    # Submit to thread pool
                    future = executor.submit(
                        self.crawl_single_item,
                        website_link_obj
                    )
                    futures.append(future)
                
                # Wait for completion and handle results
                completed = 0
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        completed += 1
                        self.stdout.write(f'Crawled {completed}/{len(futures)} items')
                    except Exception as e:
                        logger.error(f"Error in crawl worker: {str(e)}", extra=logger_extra)
                        self.stdout.write(self.style.ERROR(f'Crawl error: {str(e)}'))
            
            self.stdout.write(self.style.SUCCESS(f'Crawling completed: {completed} items processed'))
            
        except Exception as e:
            logger.error(f"Error in run_crawling: {str(e)}", extra=logger_extra)
            self.stdout.write(self.style.ERROR(f'Crawling failed: {str(e)}'))

    def run_indexing(self, num_workers, max_items):
        """Run indexing with specified number of workers"""
        try:
            logger.info("STARTED index_website_scheduler", extra=logger_extra)
            
            # Get items to index
            website_links = WebsiteLink.objects.filter(
                is_indexed=False
            )[:max_items]
            
            if not website_links.exists():
                self.stdout.write(self.style.WARNING('No items to index.'))
                return
            
            self.stdout.write(f'Indexing {website_links.count()} items with {num_workers} workers...')
            
            # Process with thread pool
            with ThreadPoolExecutor(max_workers=num_workers) as executor:
                futures = []
                
                for website_link_obj in website_links:
                    future = executor.submit(
                        self.index_single_item,
                        website_link_obj
                    )
                    futures.append(future)
                
                # Wait for completion and handle results
                completed = 0
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        completed += 1
                        self.stdout.write(f'Indexed {completed}/{len(futures)} items')
                    except Exception as e:
                        logger.error(f"Error in index worker: {str(e)}", extra=logger_extra)
                        self.stdout.write(self.style.ERROR(f'Index error: {str(e)}'))
            
            self.stdout.write(self.style.SUCCESS(f'Indexing completed: {completed} items processed'))
            
        except Exception as e:
            logger.error(f"Error in run_indexing: {str(e)}", extra=logger_extra)
            self.stdout.write(self.style.ERROR(f'Indexing failed: {str(e)}'))

    def crawl_single_item(self, website_link_obj):
        """Crawl a single website link"""
        try:
            crawl_weblink(website_link_obj, WebsiteLink, User)
            return True
        except Exception as e:
            logger.error(f"Error crawling {website_link_obj.link}: {str(e)}", extra=logger_extra)
            return False

    def index_single_item(self, website_link_obj):
        """Index a single website link"""
        try:
            index_website(website_link_obj)
            return True
        except Exception as e:
            logger.error(f"Error indexing {website_link_obj.link}: {str(e)}", extra=logger_extra)
            return False
