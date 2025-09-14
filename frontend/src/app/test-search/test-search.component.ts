import { Component, OnInit } from '@angular/core';
import { ApiServiceService } from '../api-service.service';
import { trigger, state, style, transition, animate } from '@angular/animations';

export interface ToastMessage {
  id: string;
  message: string;
  type: 'success' | 'error' | 'info' | 'warning';
  duration?: number;
}

@Component({
  selector: 'app-test-search',
  templateUrl: './test-search.component.html',
  styleUrls: ['./test-search.component.scss'],
  animations: [
    trigger('slideInOut', [
      transition(':enter', [
        style({ transform: 'translateX(100%)', opacity: 0 }),
        animate('300ms ease-in', style({ transform: 'translateX(0%)', opacity: 1 }))
      ]),
      transition(':leave', [
        animate('300ms ease-out', style({ transform: 'translateX(100%)', opacity: 0 }))
      ])
    ])
  ]
})
export class TestSearchComponent implements OnInit {

  search_results_list: any[] = [];
  resultStatus = 'empty';
  isLoading = false;
  searchTime: number | null = null;
  currentQuery = '';
  toasts: ToastMessage[] = [];

  constructor(private api: ApiServiceService) { }

  ngOnInit(): void {
  }

  onInputChange(queryInput: HTMLInputElement): void {
    this.currentQuery = queryInput.value.trim();
    
    // Clear results when user starts typing
    if (this.currentQuery === '') {
      this.search_results_list = [];
      this.resultStatus = 'empty';
    }
  }

  search(queryInput: HTMLInputElement): void {
    const query = queryInput.value.trim();
    
    if (!query) {
      this.showToast('Please enter a search query', 'warning');
      return;
    }

    this.isLoading = true;
    this.resultStatus = 'loading';
    this.search_results_list = [];
    this.searchTime = null;
    this.currentQuery = query;

    const startTime = performance.now();

    this.api.getSearchResults(query).subscribe(
      (response: any) => {
        const endTime = performance.now();
        this.searchTime = Math.round(endTime - startTime);
        
        this.search_results_list = response.query_result || [];
        this.isLoading = false;
        
        if (this.search_results_list.length === 0) {
          this.resultStatus = 'noresultfound';
          this.showToast('No results found for your search', 'info');
        } else {
          this.resultStatus = 'success';
          this.showToast(`Found ${this.search_results_list.length} results`, 'success');
        }
      },
      (error) => {
        const endTime = performance.now();
        this.searchTime = Math.round(endTime - startTime);
        
        this.isLoading = false;
        this.resultStatus = 'noresultfound';
        this.showToast('Search failed. Please try again.', 'error');
        console.error('Search error:', error);
      }
    );
  }

  copyToClipboard(text: string): void {
    if (navigator.clipboard && window.isSecureContext) {
      // Use modern clipboard API
      navigator.clipboard.writeText(text).then(() => {
        this.showToast('Link copied to clipboard!', 'success');
      }).catch(err => {
        console.error('Failed to copy: ', err);
        this.fallbackCopyToClipboard(text);
      });
    } else {
      // Fallback for older browsers
      this.fallbackCopyToClipboard(text);
    }
  }

  private fallbackCopyToClipboard(text: string): void {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
      document.execCommand('copy');
      this.showToast('Link copied to clipboard!', 'success');
    } catch (err) {
      console.error('Fallback copy failed: ', err);
      this.showToast('Failed to copy link', 'error');
    }
    
    document.body.removeChild(textArea);
  }

  // Toast functionality
  showToast(message: string, type: ToastMessage['type'] = 'info', duration: number = 3000): void {
    const id = Math.random().toString(36).substr(2, 9);
    const toast: ToastMessage = { id, message, type, duration };
    
    this.toasts.push(toast);

    // Auto remove after duration
    setTimeout(() => {
      this.removeToast(id);
    }, duration);
  }

  removeToast(id: string): void {
    this.toasts = this.toasts.filter(toast => toast.id !== id);
  }

  // Utility method to truncate text
  truncateText(text: string, maxLength: number = 150): string {
    if (text.length <= maxLength) {
      return text;
    }
    return text.substring(0, maxLength) + '...';
  }

  // Utility method to format URL
  formatUrl(url: string): string {
    try {
      const urlObj = new URL(url);
      return urlObj.hostname + urlObj.pathname;
    } catch {
      return url;
    }
  }

  // Method to clear search
  clearSearch(queryInput: HTMLInputElement): void {
    queryInput.value = '';
    this.currentQuery = '';
    this.search_results_list = [];
    this.resultStatus = 'empty';
    this.searchTime = null;
  }

  // Method to retry search
  retrySearch(queryInput: HTMLInputElement): void {
    if (this.currentQuery) {
      queryInput.value = this.currentQuery;
      this.search(queryInput);
    }
  }
}
