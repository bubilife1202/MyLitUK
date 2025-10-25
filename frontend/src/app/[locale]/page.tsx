'use client';

import { useTranslations } from 'next-intl';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import AuthorSelector from '@/components/AuthorSelector';
import PreferenceSettings from '@/components/PreferenceSettings';

export default function HomePage() {
  const t = useTranslations('home');
  const tCommon = useTranslations('common');
  const tNav = useTranslations('nav');
  const params = useParams();
  const locale = params.locale as string;

  const [authors, setAuthors] = useState([]);
  const [customAuthors, setCustomAuthors] = useState<string[]>([]);
  const [books, setBooks] = useState([]);
  const [events, setEvents] = useState([]);
  const [bookCount, setBookCount] = useState(6);
  const [eventCount, setEventCount] = useState(6);

  useEffect(() => {
    // Load preferences from localStorage (client-side only)
    if (typeof window !== 'undefined') {
      const savedBookCount = localStorage.getItem('book_display_count');
      const savedEventCount = localStorage.getItem('event_display_count');
      const savedAuthors = localStorage.getItem('preferred_authors');
      const savedCustomAuthors = localStorage.getItem('custom_authors');

      if (savedBookCount) setBookCount(parseInt(savedBookCount));
      if (savedEventCount) setEventCount(parseInt(savedEventCount));
      if (savedCustomAuthors) setCustomAuthors(JSON.parse(savedCustomAuthors));

      loadData(savedAuthors ? JSON.parse(savedAuthors) : []);
    }
  }, []);

  const loadData = (preferredAuthors: number[] = []) => {
    // 작가 목록 가져오기 (항상 전체 목록)
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/authors?size=50`)
      .then(res => res.json())
      .then(data => {
        const allAuthors = data.items || [];

        if (preferredAuthors.length > 0) {
          // 선택한 작가만 표시
          const filtered = allAuthors.filter((a: any) => preferredAuthors.includes(a.id));
          setAuthors(filtered);
        } else {
          // 선택 안 했으면 처음 6명만 표시
          setAuthors(allAuthors.slice(0, 6));
        }

        // 책 로딩 (DB에 있는 작가들만 사용)
        loadBooksFromAuthors(preferredAuthors, allAuthors);
      })
      .catch(err => console.log(err));

    // UK 문학 이벤트 가져오기
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/news/events`)
      .then(res => res.json())
      .then(data => setEvents(data.items.slice(0, eventCount) || []))
      .catch(err => console.log(err));
  };

  const loadBooksFromAuthors = (preferredAuthors: number[], allAuthors: any[]) => {
    if (typeof window !== 'undefined') {
      const savedCustomAuthors = localStorage.getItem('custom_authors');
      const customAuthorsList = savedCustomAuthors ? JSON.parse(savedCustomAuthors) : [];

      let bookPromises: Promise<any>[] = [];

      // 선택한 작가가 있으면 그들의 책만
      if (preferredAuthors.length > 0) {
        const authorIds = preferredAuthors.join(',');
        const dbBooksPromise = fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/api/latest-books/by-authors?author_ids=${authorIds}&months=6&books_per_author=2`
        )
          .then(res => res.json())
          .then(data => data.items || [])
          .catch(err => {
            console.log('Error loading DB authors books:', err);
            return [];
          });
        bookPromises.push(dbBooksPromise);
      } else if (allAuthors.length > 0) {
        // 선택 안 했으면 DB에 있는 모든 작가들의 책 (처음 10명)
        const authorIds = allAuthors.slice(0, 10).map((a: any) => a.id).join(',');
        const dbBooksPromise = fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/api/latest-books/by-authors?author_ids=${authorIds}&months=6&books_per_author=1`
        )
          .then(res => res.json())
          .then(data => data.items || [])
          .catch(err => {
            console.log('Error loading DB authors books:', err);
            return [];
          });
        bookPromises.push(dbBooksPromise);
      }

      // 커스텀 작가들의 최신 책
      if (customAuthorsList.length > 0) {
        const authorNames = customAuthorsList.join(',');
        const customBooksPromise = fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/api/latest-books/by-custom-authors?author_names=${encodeURIComponent(authorNames)}&months=6&books_per_author=2`
        )
          .then(res => res.json())
          .then(data => data.items || [])
          .catch(err => {
            console.log('Error loading custom authors books:', err);
            return [];
          });
        bookPromises.push(customBooksPromise);
      }

      // 모든 책 합치기
      if (bookPromises.length > 0) {
        Promise.all(bookPromises).then(results => {
          const allBooks = results.flat();
          // 출간일 기준 최신순 정렬
          allBooks.sort((a: any, b: any) => {
            return (b.publication_date || '').localeCompare(a.publication_date || '');
          });
          setBooks(allBooks.slice(0, bookCount));
        });
      } else {
        setBooks([]);
      }
    }
  };

  const handlePreferencesChange = () => {
    if (typeof window !== 'undefined') {
      const savedAuthors = localStorage.getItem('preferred_authors');
      const savedCustomAuthors = localStorage.getItem('custom_authors');
      if (savedCustomAuthors) setCustomAuthors(JSON.parse(savedCustomAuthors));
      loadData(savedAuthors ? JSON.parse(savedAuthors) : []);
    }
  };

  const generateBookstoreLinks = (title: string, author: string, isbn?: string) => {
    const cleanISBN = isbn ? isbn.replace(/-/g, '') : null;

    return {
      waterstones: cleanISBN
        ? `https://www.waterstones.com/book/${cleanISBN}`
        : `https://www.waterstones.com/books/search/term/${encodeURIComponent(title)}`,

      amazon: cleanISBN
        ? `https://www.amazon.co.uk/dp/${cleanISBN}`
        : `https://www.amazon.co.uk/s?k=${encodeURIComponent(title + ' ' + author)}`,

      bookshop: cleanISBN
        ? `https://uk.bookshop.org/books?keywords=${cleanISBN}`
        : `https://uk.bookshop.org/search?keywords=${encodeURIComponent(title)}`
    };
  };

  const formatDate = (dateStr: string) => {
    try {
      const date = new Date(dateStr);
      return date.toLocaleDateString(locale === 'ko' ? 'ko-KR' : 'en-GB', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    } catch {
      return dateStr;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation - Mobile Optimized */}
      <nav className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-xl sm:text-2xl font-bold text-primary-600 flex items-center gap-2">
                <span className="text-2xl">🇬🇧</span>
                <span className="hidden sm:inline">{t('title')}</span>
                <span className="sm:hidden">MyLitUK</span>
              </h1>
            </div>
            <div className="flex items-center gap-1 sm:gap-3">
              <PreferenceSettings locale={locale} onSave={handlePreferencesChange} />
              <AuthorSelector locale={locale} onSave={handlePreferencesChange} />
              <Link href={`/${locale}/login`} className="hidden sm:inline text-sm text-gray-700 hover:text-primary-600">
                {tNav('login')}
              </Link>
              <Link href={`/${locale}/register`} className="btn-primary text-xs sm:text-sm px-3 py-2 min-h-[40px]">
                {tNav('register')}
              </Link>
              <select
                value={locale}
                onChange={(e) => {
                  const newLocale = e.target.value;
                  window.location.href = `/${newLocale}`;
                }}
                className="px-2 py-2 border border-gray-300 rounded-md text-xs sm:text-sm min-h-[40px]"
              >
                <option value="en">EN</option>
                <option value="ko">KO</option>
              </select>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section - UK Themed */}
      <div className="bg-gradient-to-br from-blue-900 via-blue-800 to-red-800 text-white relative overflow-hidden">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAxMCAwIEwgMCAwIDAgMTAiIGZpbGw9Im5vbmUiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMC41IiBvcGFjaXR5PSIwLjEiLz48L3BhdHRlcm4+PC9kZWZzPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9InVybCgjZ3JpZCkiLz48L3N2Zz4=')] opacity-30"></div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-20 md:py-28 relative">
          <div className="text-center">
            <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold mb-4 sm:mb-6">
              {t('subtitle')}
            </h1>
            <p className="text-lg sm:text-xl md:text-2xl mb-8 sm:mb-10 max-w-3xl mx-auto px-4 font-light">
              {t('description')}
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Link
                href={`/${locale}/register`}
                className="w-full sm:w-auto bg-white text-blue-900 px-8 py-4 rounded-lg font-bold hover:bg-gray-100 transition-all shadow-lg hover:shadow-xl text-base sm:text-lg min-h-[56px] flex items-center justify-center"
              >
                {t('cta.button')}
              </Link>
              <Link
                href={`/${locale}/books`}
                className="w-full sm:w-auto bg-transparent border-2 border-white text-white px-8 py-4 rounded-lg font-semibold hover:bg-white hover:text-blue-900 transition-all text-base sm:text-lg min-h-[56px] flex items-center justify-center"
              >
                {locale === 'ko' ? '책 둘러보기' : 'Explore Books'}
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section - Mobile Optimized */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16">
        <h2 className="text-3xl sm:text-4xl font-bold text-center mb-10 sm:mb-14 text-gray-900">
          {t('features.title')}
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8">
          <div className="bg-white p-6 sm:p-8 rounded-2xl shadow-lg hover:shadow-xl transition-shadow text-center">
            <div className="text-5xl mb-4">📚</div>
            <h3 className="text-xl sm:text-2xl font-bold mb-3 text-gray-900">{t('features.personalized.title')}</h3>
            <p className="text-base text-gray-600 leading-relaxed">{t('features.personalized.description')}</p>
          </div>
          <div className="bg-white p-6 sm:p-8 rounded-2xl shadow-lg hover:shadow-xl transition-shadow text-center">
            <div className="text-5xl mb-4">🔔</div>
            <h3 className="text-xl sm:text-2xl font-bold mb-3 text-gray-900">{t('features.alerts.title')}</h3>
            <p className="text-base text-gray-600 leading-relaxed">{t('features.alerts.description')}</p>
          </div>
          <div className="bg-white p-6 sm:p-8 rounded-2xl shadow-lg hover:shadow-xl transition-shadow text-center">
            <div className="text-5xl mb-4">🌐</div>
            <h3 className="text-xl sm:text-2xl font-bold mb-3 text-gray-900">{t('features.multilingual.title')}</h3>
            <p className="text-base text-gray-600 leading-relaxed">{t('features.multilingual.description')}</p>
          </div>
        </div>
      </div>

      {/* Authors Section - Mobile Optimized */}
      <div className="bg-white py-12 sm:py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl sm:text-4xl font-bold mb-8 sm:mb-12 text-gray-900">
            {locale === 'ko' ? '주목할 만한 영국 작가들' : 'Featured UK Authors'}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {authors.map((author: any) => (
              <div key={author.id} className="bg-gray-50 p-6 rounded-xl hover:shadow-lg transition-all border border-gray-200">
                <h3 className="text-xl font-bold mb-3 text-gray-900">
                  {locale === 'ko' && author.name_ko ? author.name_ko : author.name}
                </h3>
                <p className="text-gray-600 text-sm leading-relaxed line-clamp-3">
                  {locale === 'ko' && author.bio_ko ? author.bio_ko : author.bio}
                </p>
              </div>
            ))}
            {customAuthors.map((name: string, idx: number) => (
              <div key={`custom-${idx}`} className="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-xl border-2 border-blue-300 hover:shadow-lg transition-all">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-xl font-bold text-blue-900">{name}</h3>
                  <span className="text-xs bg-blue-200 text-blue-800 px-3 py-1 rounded-full font-semibold">
                    {locale === 'ko' ? '직접 추가' : 'Custom'}
                  </span>
                </div>
                <p className="text-blue-700 text-sm italic">
                  {locale === 'ko' ? '관심 작가로 추가하셨습니다' : 'Added to your favorites'}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Books Section with Bookstore Links - Mobile Optimized */}
      <div className="bg-gray-100 py-12 sm:py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-8 sm:mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900">
              {locale === 'ko' ? '최신 출간 도서 (6개월 이내)' : 'Latest UK Books (Last 6 Months)'}
            </h2>
            <p className="text-sm text-gray-600 mt-2">
              {locale === 'ko'
                ? '📡 Google Books API에서 실시간으로 가져온 최신 정보입니다'
                : '📡 Real-time data from Google Books API'}
            </p>
          </div>
          {books.length === 0 ? (
            <div className="col-span-full text-center py-12">
              <p className="text-gray-500 text-lg">
                {locale === 'ko'
                  ? '📚 선택한 작가의 최신 출간 도서를 불러오는 중입니다...'
                  : '📚 Loading latest books from your selected authors...'}
              </p>
              <p className="text-sm text-gray-400 mt-2">
                {locale === 'ko'
                  ? '작가를 선택하면 해당 작가의 6개월 이내 신간이 표시됩니다'
                  : 'Select authors to see their latest books from the past 6 months'}
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {books.map((book: any, index: number) => {
              const bookstoreLinks = generateBookstoreLinks(
                book.title,
                book.author_name || 'Unknown',
                book.isbn
              );

              // Format publication date
              const pubDate = book.publication_date ? formatDate(book.publication_date) : '';

              return (
                <div key={book.isbn || `${book.title}-${index}`} className="bg-white p-6 rounded-xl shadow-md hover:shadow-xl transition-all">
                  {/* New Badge */}
                  {book.publication_date && (
                    <div className="mb-2">
                      <span className="inline-block px-2 py-1 bg-green-100 text-green-800 text-xs font-semibold rounded">
                        {locale === 'ko' ? '신간' : 'NEW'} {pubDate}
                      </span>
                    </div>
                  )}

                  <h3 className="text-lg font-bold mb-2 text-gray-900 line-clamp-2">
                    {locale === 'ko' && book.title_ko ? book.title_ko : book.title}
                  </h3>
                  <p className="text-sm text-gray-600 mb-2">
                    {locale === 'ko' ? '저자' : 'by'} <span className="font-semibold">{book.author_name || 'Unknown'}</span>
                  </p>
                  {book.publisher && (
                    <p className="text-xs text-gray-500 mb-3">
                      {book.publisher}
                    </p>
                  )}
                  <p className="text-gray-600 text-sm leading-relaxed line-clamp-3 mb-4">
                    {locale === 'ko' && book.description_ko ? book.description_ko : book.description}
                  </p>

                  {/* Bookstore Links */}
                  <div className="pt-4 border-t border-gray-200">
                    <p className="text-xs font-semibold text-gray-700 mb-2 flex items-center justify-between">
                      <span>{locale === 'ko' ? '🛒 구매하기' : '🛒 Buy from'}</span>
                      {book.isbn && (
                        <span className="text-xs font-normal text-gray-500">ISBN: {book.isbn}</span>
                      )}
                    </p>
                    <div className="flex flex-wrap gap-2">
                      <a
                        href={bookstoreLinks.waterstones}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-block px-3 py-1.5 bg-blue-600 text-white text-xs rounded-md hover:bg-blue-700 transition-colors font-medium"
                        title={book.isbn ? `Direct link with ISBN ${book.isbn}` : 'Search by title'}
                      >
                        Waterstones
                      </a>
                      <a
                        href={bookstoreLinks.amazon}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-block px-3 py-1.5 bg-orange-500 text-white text-xs rounded-md hover:bg-orange-600 transition-colors font-medium"
                        title={book.isbn ? `Direct link with ISBN ${book.isbn}` : 'Search by title'}
                      >
                        Amazon UK
                      </a>
                      <a
                        href={bookstoreLinks.bookshop}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-block px-3 py-1.5 bg-green-600 text-white text-xs rounded-md hover:bg-green-700 transition-colors font-medium"
                        title={book.isbn ? `Search with ISBN ${book.isbn}` : 'Search by title'}
                      >
                        Bookshop.org
                      </a>
                    </div>
                  </div>
                </div>
              );
            })}
            </div>
          )}
        </div>
      </div>

      {/* UK Literary Events Section - Mobile Optimized */}
      <div className="bg-white py-12 sm:py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl sm:text-4xl font-bold mb-8 sm:mb-12 text-gray-900">
            {locale === 'ko' ? '🎭 다가오는 영국 문학 이벤트' : '🎭 Upcoming UK Literary Events'}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {events.map((event: any, idx: number) => (
              <div key={idx} className="bg-gradient-to-br from-red-50 to-blue-50 p-6 rounded-xl shadow-md hover:shadow-xl transition-all border border-gray-200">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xs font-bold text-blue-800 bg-blue-200 px-3 py-1 rounded-full">
                    {event.category || 'Festival'}
                  </span>
                  {event.date && (
                    <span className="text-xs text-gray-600">
                      📅 {formatDate(event.date)}
                    </span>
                  )}
                </div>
                <h3 className="text-lg font-bold mb-2 text-gray-900">{event.name}</h3>
                <p className="text-sm text-gray-600 mb-3 flex items-center gap-1">
                  📍 {event.location}
                </p>
                <p className="text-gray-700 text-sm leading-relaxed line-clamp-3 mb-4">
                  {event.description}
                </p>
                {event.url && (
                  <a
                    href={event.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-block text-sm font-semibold text-blue-600 hover:text-blue-800 hover:underline"
                  >
                    {locale === 'ko' ? '더 알아보기 →' : 'Learn more →'}
                  </a>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section - Mobile Optimized */}
      <div className="bg-gradient-to-r from-blue-900 to-red-900 py-16 sm:py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-white">
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">{t('cta.title')}</h2>
          <p className="text-lg sm:text-xl mb-8 font-light">
            {t('cta.description')}
          </p>
          <Link
            href={`/${locale}/register`}
            className="inline-block bg-white text-blue-900 px-10 py-4 rounded-lg font-bold hover:bg-gray-100 transition-all shadow-lg text-lg min-h-[56px] flex items-center justify-center max-w-xs mx-auto"
          >
            {t('cta.button')}
          </Link>
        </div>
      </div>

      {/* Footer - Mobile Optimized */}
      <footer className="bg-gray-900 text-white py-8 sm:py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex items-center justify-center gap-3 mb-4">
              <span className="text-3xl">🇬🇧</span>
              <h3 className="text-2xl font-bold">MyLitUK</h3>
            </div>
            <p className="text-sm sm:text-base mb-4 text-gray-400">
              {locale === 'ko'
                ? '영국 문학을 사랑하는 사람들을 위한 플랫폼'
                : 'Your gateway to UK literature'}
            </p>
            <p className="text-xs text-gray-500 mb-2">
              &copy; 2025 MyLitUK. All rights reserved.
            </p>
            <p className="text-xs text-gray-400">
              v4.0.0 | {locale === 'ko' ? '로그인 없이 개인화 가능' : 'Personalized without login'} |{' '}
              <a href="https://mylituk-api.onrender.com/docs" target="_blank" rel="noopener noreferrer" className="hover:text-white underline">
                API Docs
              </a>
            </p>
            <div className="mt-4 pt-4 border-t border-gray-800">
              <p className="text-xs text-gray-500">
                {locale === 'ko'
                  ? '📚 독서 리스트 | ⭐ 리뷰 | 🎯 챌린지 | 👥 커뮤니티 | 🛒 영국 서점 링크 | 📰 실시간 뉴스'
                  : '📚 Reading Lists | ⭐ Reviews | 🎯 Challenges | 👥 Community | 🛒 UK Bookstores | 📰 Live News'
                }
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
