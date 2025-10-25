'use client';

import { useState, useEffect } from 'react';

interface PreferenceSettingsProps {
  locale: string;
  onSave?: () => void;
}

export default function PreferenceSettings({ locale, onSave }: PreferenceSettingsProps) {
  const [bookCount, setBookCount] = useState(6);
  const [eventCount, setEventCount] = useState(6);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    // Load saved preferences (client-side only)
    if (typeof window !== 'undefined') {
      const savedBookCount = localStorage.getItem('book_display_count');
      const savedEventCount = localStorage.getItem('event_display_count');

      if (savedBookCount) setBookCount(parseInt(savedBookCount));
      if (savedEventCount) setEventCount(parseInt(savedEventCount));
    }
  }, []);

  const saveSettings = () => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('book_display_count', bookCount.toString());
      localStorage.setItem('event_display_count', eventCount.toString());
    }
    setIsOpen(false);
    if (onSave) onSave();
  };

  return (
    <div>
      {/* Trigger Button - Mobile Optimized */}
      <button
        onClick={() => setIsOpen(true)}
        className="text-xs sm:text-sm text-gray-700 hover:text-primary-600 px-2 py-2 min-h-[44px] flex items-center justify-center"
      >
        <span className="hidden sm:inline">⚙️ </span>
        {locale === 'ko' ? '설정' : 'Settings'}
      </button>

      {/* Modal - Mobile Optimized */}
      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-end sm:items-center justify-center">
          <div className="bg-white rounded-t-2xl sm:rounded-lg w-full sm:max-w-md p-6 sm:p-8">
            {/* Header - Mobile Optimized */}
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-2xl font-bold text-gray-900">
                {locale === 'ko' ? '표시 설정' : 'Display Settings'}
              </h3>
              <button
                onClick={() => setIsOpen(false)}
                className="sm:hidden text-2xl text-gray-500 w-10 h-10 flex items-center justify-center"
                aria-label="Close"
              >
                ×
              </button>
            </div>

            <div className="space-y-6">
              {/* Book Count - Mobile Optimized */}
              <div>
                <label className="block text-base font-semibold mb-3 text-gray-900">
                  {locale === 'ko' ? '📚 책 표시 갯수' : '📚 Books to Display'}
                </label>
                <select
                  value={bookCount}
                  onChange={(e) => setBookCount(parseInt(e.target.value))}
                  className="w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg focus:border-primary-600 focus:ring-2 focus:ring-primary-200 min-h-[48px]"
                >
                  <option value="3">3</option>
                  <option value="6">6</option>
                  <option value="9">9</option>
                  <option value="12">12</option>
                  <option value="15">15</option>
                  <option value="20">20</option>
                </select>
              </div>

              {/* Event Count - Mobile Optimized */}
              <div>
                <label className="block text-base font-semibold mb-3 text-gray-900">
                  {locale === 'ko' ? '🎭 이벤트 표시 갯수' : '🎭 Events to Display'}
                </label>
                <select
                  value={eventCount}
                  onChange={(e) => setEventCount(parseInt(e.target.value))}
                  className="w-full px-4 py-3 text-base border-2 border-gray-300 rounded-lg focus:border-primary-600 focus:ring-2 focus:ring-primary-200 min-h-[48px]"
                >
                  <option value="3">3</option>
                  <option value="6">6</option>
                  <option value="9">9</option>
                  <option value="12">12</option>
                </select>
              </div>
            </div>

            {/* Footer - Mobile Optimized */}
            <div className="mt-8 flex flex-col sm:flex-row justify-end gap-3">
              <button
                onClick={() => setIsOpen(false)}
                className="hidden sm:block px-6 py-3 border-2 border-gray-300 rounded-lg hover:bg-gray-50 font-semibold min-h-[48px]"
              >
                {locale === 'ko' ? '취소' : 'Cancel'}
              </button>
              <button
                onClick={saveSettings}
                className="w-full sm:w-auto btn-primary px-8 py-3 font-bold min-h-[48px]"
              >
                {locale === 'ko' ? '💾 저장' : '💾 Save'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
