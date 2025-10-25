'use client';

import { useState, useEffect } from 'react';

interface Author {
  id: number;
  name: string;
  name_ko?: string;
}

interface AuthorSelectorProps {
  locale: string;
  onSave?: () => void;
}

export default function AuthorSelector({ locale, onSave }: AuthorSelectorProps) {
  const [availableAuthors, setAvailableAuthors] = useState<Author[]>([]);
  const [selectedAuthors, setSelectedAuthors] = useState<number[]>([]);
  const [customAuthors, setCustomAuthors] = useState<string[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [customAuthorInput, setCustomAuthorInput] = useState('');

  useEffect(() => {
    // Load saved preferences (client-side only)
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('preferred_authors');
      if (saved) {
        setSelectedAuthors(JSON.parse(saved));
      }
      const savedCustom = localStorage.getItem('custom_authors');
      if (savedCustom) {
        setCustomAuthors(JSON.parse(savedCustom));
      }
    }

    // Load available authors
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/authors?size=50`)
      .then(res => res.json())
      .then(data => setAvailableAuthors(data.items || []))
      .catch(err => console.error('Failed to load authors:', err));
  }, []);

  const toggleAuthor = (authorId: number) => {
    const newSelected = selectedAuthors.includes(authorId)
      ? selectedAuthors.filter(id => id !== authorId)
      : [...selectedAuthors, authorId];

    setSelectedAuthors(newSelected);
    if (typeof window !== 'undefined') {
      localStorage.setItem('preferred_authors', JSON.stringify(newSelected));
    }
  };

  const addCustomAuthor = () => {
    const trimmed = customAuthorInput.trim();
    if (trimmed && !customAuthors.includes(trimmed)) {
      const newCustom = [...customAuthors, trimmed];
      setCustomAuthors(newCustom);
      if (typeof window !== 'undefined') {
        localStorage.setItem('custom_authors', JSON.stringify(newCustom));
      }
      setCustomAuthorInput('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      addCustomAuthor();
    }
  };

  const removeCustomAuthor = (authorName: string) => {
    const newCustom = customAuthors.filter(name => name !== authorName);
    setCustomAuthors(newCustom);
    if (typeof window !== 'undefined') {
      localStorage.setItem('custom_authors', JSON.stringify(newCustom));
    }
  };

  const saveAndClose = () => {
    setIsOpen(false);
    if (onSave) onSave();
  };

  const selectAll = () => {
    const allIds = filteredAuthors.map(a => a.id);
    const newSelected = Array.from(new Set([...selectedAuthors, ...allIds]));
    setSelectedAuthors(newSelected);
    if (typeof window !== 'undefined') {
      localStorage.setItem('preferred_authors', JSON.stringify(newSelected));
    }
  };

  const deselectAll = () => {
    const filteredIds = new Set(filteredAuthors.map(a => a.id));
    const newSelected = selectedAuthors.filter(id => !filteredIds.has(id));
    setSelectedAuthors(newSelected);
    if (typeof window !== 'undefined') {
      localStorage.setItem('preferred_authors', JSON.stringify(newSelected));
    }
  };

  const filteredAuthors = availableAuthors.filter(author =>
    author.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (author.name_ko && author.name_ko.includes(searchTerm))
  );

  const selectedAuthorsList = availableAuthors.filter(a => selectedAuthors.includes(a.id));
  const totalSelectedCount = selectedAuthors.length + customAuthors.length;

  return (
    <div className="relative">
      {/* Trigger Button - Mobile Optimized */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="btn-primary text-xs sm:text-sm px-2 py-2 sm:px-4 sm:py-2 min-h-[44px] flex items-center justify-center"
      >
        <span className="hidden sm:inline">📖 </span>
        {locale === 'ko' ? '작가' : 'Authors'} ({totalSelectedCount})
      </button>

      {/* Selected Authors Preview - Hidden on mobile */}
      {(selectedAuthorsList.length > 0 || customAuthors.length > 0) && !isOpen && (
        <div className="hidden sm:block mt-2 text-xs text-gray-600">
          {locale === 'ko' ? '팔로우 중: ' : 'Following: '}
          {[
            ...selectedAuthorsList.slice(0, 2).map(a => locale === 'ko' && a.name_ko ? a.name_ko : a.name),
            ...customAuthors.slice(0, 2)
          ].join(', ')}
          {totalSelectedCount > 2 && ` +${totalSelectedCount - 2}`}
        </div>
      )}

      {/* Modal - Mobile Optimized */}
      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-end sm:items-center justify-center">
          <div className="bg-white rounded-t-2xl sm:rounded-lg w-full sm:max-w-2xl h-[95vh] sm:h-auto sm:max-h-[90vh] overflow-hidden flex flex-col">
            {/* Header - Mobile Optimized */}
            <div className="p-3 sm:p-4 border-b sticky top-0 bg-white z-10">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-lg sm:text-xl font-bold">
                  {locale === 'ko' ? '작가 선택' : 'Choose Authors'}
                </h3>
                <button
                  onClick={() => setIsOpen(false)}
                  className="sm:hidden text-2xl text-gray-500 w-10 h-10 flex items-center justify-center"
                  aria-label="Close"
                >
                  ×
                </button>
              </div>

              {/* Custom Author Input - Mobile Optimized */}
              <div className="mb-3">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {locale === 'ko' ? '직접 입력하기' : 'Add Custom Author'}
                </label>
                <div className="flex flex-col sm:flex-row gap-2">
                  <input
                    type="text"
                    placeholder={locale === 'ko' ? '작가 이름 입력...' : 'Enter author name...'}
                    value={customAuthorInput}
                    onChange={(e) => setCustomAuthorInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    className="flex-1 px-4 py-3 text-base border rounded-md min-h-[44px]"
                  />
                  <button
                    onClick={addCustomAuthor}
                    className="w-full sm:w-auto px-6 py-3 bg-primary-600 text-white rounded-md hover:bg-primary-700 font-medium min-h-[44px]"
                  >
                    {locale === 'ko' ? '추가' : 'Add'}
                  </button>
                </div>
              </div>

              {/* Custom Authors List - Mobile Optimized */}
              {customAuthors.length > 0 && (
                <div className="mb-3">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {locale === 'ko' ? '내가 추가한 작가' : 'My Custom Authors'}
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {customAuthors.map((name, idx) => (
                      <span
                        key={idx}
                        className="inline-flex items-center px-3 py-2 bg-primary-100 text-primary-800 rounded-full text-sm"
                      >
                        {name}
                        <button
                          onClick={() => removeCustomAuthor(name)}
                          className="ml-2 text-primary-600 hover:text-primary-900 text-xl w-6 h-6 flex items-center justify-center"
                          aria-label={`Remove ${name}`}
                        >
                          ×
                        </button>
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Search in Database - Enhanced Search with Clear Button */}
              <div className="relative">
                <input
                  type="text"
                  placeholder={locale === 'ko' ? '🔍 작가 이름으로 검색... (50+ 작가)' : '🔍 Search by author name... (50+ authors)'}
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full px-4 py-3 pr-20 text-base border-2 border-gray-300 rounded-md focus:border-primary-600 focus:ring-2 focus:ring-primary-200 min-h-[44px]"
                />
                {searchTerm && (
                  <button
                    onClick={() => setSearchTerm('')}
                    className="absolute right-2 top-1/2 -translate-y-1/2 px-3 py-1 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded"
                    aria-label="Clear search"
                  >
                    ✕
                  </button>
                )}
              </div>
              {searchTerm && (
                <div className="mt-2 text-sm text-gray-600">
                  {locale === 'ko' ? `${filteredAuthors.length}명 찾음` : `${filteredAuthors.length} found`}
                </div>
              )}

              {/* Quick Select Buttons */}
              {filteredAuthors.length > 0 && (
                <div className="mt-3 flex gap-2">
                  <button
                    onClick={selectAll}
                    className="flex-1 px-3 py-2 text-sm bg-primary-100 text-primary-700 rounded-md hover:bg-primary-200 font-medium min-h-[40px]"
                  >
                    {locale === 'ko' ? '✓ 모두 선택' : '✓ Select All'}
                  </button>
                  <button
                    onClick={deselectAll}
                    className="flex-1 px-3 py-2 text-sm bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 font-medium min-h-[40px]"
                  >
                    {locale === 'ko' ? '✕ 모두 해제' : '✕ Deselect All'}
                  </button>
                </div>
              )}
            </div>

            {/* Author List from Database - Mobile Optimized */}
            <div className="flex-1 overflow-y-auto p-3 sm:p-4 overscroll-contain">
              <div className="grid grid-cols-1 gap-3">
                {filteredAuthors.map(author => (
                  <label
                    key={author.id}
                    className={`flex items-center p-4 border-2 rounded-xl cursor-pointer active:scale-98 transition-transform ${
                      selectedAuthors.includes(author.id) ? 'border-primary-600 bg-primary-50' : 'border-gray-300'
                    }`}
                  >
                    <input
                      type="checkbox"
                      checked={selectedAuthors.includes(author.id)}
                      onChange={() => toggleAuthor(author.id)}
                      className="mr-4 w-6 h-6 min-w-[24px]"
                    />
                    <span className="font-medium text-base">
                      {locale === 'ko' && author.name_ko ? author.name_ko : author.name}
                    </span>
                  </label>
                ))}
              </div>
              {filteredAuthors.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  <div className="text-4xl mb-3">🔍</div>
                  <div className="font-medium">
                    {locale === 'ko' ? '검색 결과가 없습니다' : 'No authors found'}
                  </div>
                  <div className="text-sm mt-2">
                    {locale === 'ko'
                      ? '다른 작가를 검색하거나 "직접 입력하기"로 추가하세요'
                      : 'Try a different search or use "Add Custom Author"'}
                  </div>
                </div>
              )}
            </div>

            {/* Footer - Mobile Optimized */}
            <div className="p-3 sm:p-4 border-t bg-white sticky bottom-0">
              <div className="flex flex-col sm:flex-row justify-between items-stretch sm:items-center gap-3">
                <span className="text-sm text-gray-600 text-center sm:text-left">
                  {totalSelectedCount} {locale === 'ko' ? '명 선택됨' : 'selected'}
                </span>
                <div className="flex gap-2">
                  <button
                    onClick={() => setIsOpen(false)}
                    className="hidden sm:block flex-1 sm:flex-none px-4 py-3 border-2 border-gray-300 rounded-md hover:bg-gray-50 font-medium min-h-[44px]"
                  >
                    {locale === 'ko' ? '취소' : 'Cancel'}
                  </button>
                  <button
                    onClick={saveAndClose}
                    className="flex-1 sm:flex-none btn-primary px-6 py-3 font-medium min-h-[44px]"
                  >
                    {locale === 'ko' ? '저장' : 'Save'}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
