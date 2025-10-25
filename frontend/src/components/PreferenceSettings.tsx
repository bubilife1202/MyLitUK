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
    // Load saved preferences
    const savedBookCount = localStorage.getItem('book_display_count');
    const savedEventCount = localStorage.getItem('event_display_count');

    if (savedBookCount) setBookCount(parseInt(savedBookCount));
    if (savedEventCount) setEventCount(parseInt(savedEventCount));
  }, []);

  const saveSettings = () => {
    localStorage.setItem('book_display_count', bookCount.toString());
    localStorage.setItem('event_display_count', eventCount.toString());
    setIsOpen(false);
    if (onSave) onSave();
  };

  return (
    <div>
      <button
        onClick={() => setIsOpen(true)}
        className="text-sm text-gray-700 hover:text-primary-600"
      >
        ⚙️ {locale === 'ko' ? '설정' : 'Settings'}
      </button>

      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-xl font-bold mb-4">
              {locale === 'ko' ? '표시 설정' : 'Display Settings'}
            </h3>

            <div className="space-y-4">
              {/* Book Count */}
              <div>
                <label className="block text-sm font-medium mb-2">
                  {locale === 'ko' ? '책 표시 갯수' : 'Books to Display'}
                </label>
                <select
                  value={bookCount}
                  onChange={(e) => setBookCount(parseInt(e.target.value))}
                  className="w-full px-3 py-2 border rounded-md"
                >
                  <option value="3">3</option>
                  <option value="6">6</option>
                  <option value="9">9</option>
                  <option value="12">12</option>
                  <option value="15">15</option>
                  <option value="20">20</option>
                </select>
              </div>

              {/* Event Count */}
              <div>
                <label className="block text-sm font-medium mb-2">
                  {locale === 'ko' ? '이벤트 표시 갯수' : 'Events to Display'}
                </label>
                <select
                  value={eventCount}
                  onChange={(e) => setEventCount(parseInt(e.target.value))}
                  className="w-full px-3 py-2 border rounded-md"
                >
                  <option value="3">3</option>
                  <option value="6">6</option>
                  <option value="9">9</option>
                  <option value="12">12</option>
                </select>
              </div>
            </div>

            <div className="mt-6 flex justify-end space-x-2">
              <button
                onClick={() => setIsOpen(false)}
                className="px-4 py-2 border rounded-md hover:bg-gray-50"
              >
                {locale === 'ko' ? '취소' : 'Cancel'}
              </button>
              <button
                onClick={saveSettings}
                className="btn-primary"
              >
                {locale === 'ko' ? '저장' : 'Save'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
