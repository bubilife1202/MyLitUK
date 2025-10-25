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

      if (savedBookCount) setBookCount(parseInt(savedBookCount));
      if (savedEventCount) setEventCount(parseInt(savedEventCount));

      loadData(savedAuthors ? JSON.parse(savedAuthors) : []);
    }
  }, []);

  const loadData = (preferredAuthors: number[] = []) => {
    // 작가 목록 가져오기
    const authorSize = preferredAuthors.length > 0 ? preferredAuthors.length : 6;
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/authors?size=${authorSize}`)
      .then(res => res.json())
      .then(data => {
        if (preferredAuthors.length > 0) {
          // 선택한 작가만 표시
          const filtered = data.items.filter((a: any) => preferredAuthors.includes(a.id));
          setAuthors(filtered);
        } else {
          setAuthors(data.items || []);
        }
      })
      .catch(err => console.log(err));

    // 책 목록 가져오기
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/books/new?size=${bookCount}`)
      .then(res => res.json())
      .then(data => setBooks(data.items || []))
      .catch(err => console.log(err));

    // 이벤트 목록 가져오기
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/events?upcoming=true&size=${eventCount}`)
      .then(res => res.json())
      .then(data => setEvents(data.items || []))
      .catch(err => console.log(err));
  };

  const handlePreferencesChange = () => {
    if (typeof window !== 'undefined') {
      const savedAuthors = localStorage.getItem('preferred_authors');
      loadData(savedAuthors ? JSON.parse(savedAuthors) : []);
    }
  };

  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-14 sm:h-16">
            <div className="flex items-center">
              <h1 className="text-lg sm:text-2xl font-bold text-primary-600">{t('title')}</h1>
            </div>
            <div className="flex items-center space-x-2 sm:space-x-4">
              <PreferenceSettings locale={locale} onSave={handlePreferencesChange} />
              <AuthorSelector locale={locale} onSave={handlePreferencesChange} />
              <Link href={`/${locale}/login`} className="text-sm sm:text-base text-gray-700 hover:text-primary-600">
                {tNav('login')}
              </Link>
              <Link href={`/${locale}/register`} className="btn-primary text-xs sm:text-sm">
                {tNav('register')}
              </Link>
              <select
                value={locale}
                onChange={(e) => {
                  const newLocale = e.target.value;
                  window.location.href = `/${newLocale}`;
                }}
                className="px-2 py-1 sm:px-3 sm:py-1.5 border border-gray-300 rounded-md text-sm"
              >
                <option value="en">EN</option>
                <option value="ko">KO</option>
              </select>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 md:py-24">
          <div className="text-center">
            <h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold mb-3 sm:mb-4">{t('subtitle')}</h1>
            <p className="text-base sm:text-lg md:text-xl mb-6 sm:mb-8 max-w-3xl mx-auto px-4">{t('description')}</p>
            <Link href={`/${locale}/register`} className="inline-block bg-white text-primary-600 px-6 py-2.5 sm:px-8 sm:py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors text-sm sm:text-base touch-action">
              {t('cta.button')}
            </Link>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 md:py-16">
        <h2 className="text-2xl sm:text-3xl font-bold text-center mb-8 sm:mb-12">{t('features.title')}</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 sm:gap-6 md:gap-8">
          <div className="card text-center">
            <div className="text-3xl sm:text-4xl mb-3 sm:mb-4">📚</div>
            <h3 className="text-lg sm:text-xl font-semibold mb-2">{t('features.personalized.title')}</h3>
            <p className="text-sm sm:text-base text-gray-600">{t('features.personalized.description')}</p>
          </div>
          <div className="card text-center">
            <div className="text-3xl sm:text-4xl mb-3 sm:mb-4">🔔</div>
            <h3 className="text-lg sm:text-xl font-semibold mb-2">{t('features.alerts.title')}</h3>
            <p className="text-sm sm:text-base text-gray-600">{t('features.alerts.description')}</p>
          </div>
          <div className="card text-center sm:col-span-2 md:col-span-1">
            <div className="text-3xl sm:text-4xl mb-3 sm:mb-4">🌐</div>
            <h3 className="text-lg sm:text-xl font-semibold mb-2">{t('features.multilingual.title')}</h3>
            <p className="text-sm sm:text-base text-gray-600">{t('features.multilingual.description')}</p>
          </div>
        </div>
      </div>

      {/* Authors Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 md:py-16">
        <h2 className="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8">Featured UK Authors</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 sm:gap-6">
          {authors.map((author: any) => (
            <div key={author.id} className="card hover:scale-105 transition-transform">
              <h3 className="text-lg sm:text-xl font-semibold mb-2">{locale === 'ko' && author.name_ko ? author.name_ko : author.name}</h3>
              <p className="text-gray-600 text-xs sm:text-sm line-clamp-3">{locale === 'ko' && author.bio_ko ? author.bio_ko : author.bio}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Books Section */}
      <div className="bg-gray-50 py-8 sm:py-12 md:py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8">Latest Books</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 sm:gap-6">
            {books.map((book: any) => (
              <div key={book.id} className="card hover:scale-105 transition-transform">
                <h3 className="text-base sm:text-lg font-semibold mb-2">{locale === 'ko' && book.title_ko ? book.title_ko : book.title}</h3>
                <p className="text-xs sm:text-sm text-gray-500 mb-2">by {book.author_name}</p>
                <p className="text-gray-600 text-xs sm:text-sm line-clamp-2">{locale === 'ko' && book.description_ko ? book.description_ko : book.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Events Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 md:py-16">
        <h2 className="text-2xl sm:text-3xl font-bold mb-6 sm:mb-8">Upcoming Events</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 sm:gap-6">
          {events.map((event: any) => (
            <div key={event.id} className="card hover:scale-105 transition-transform">
              <div className="text-xs sm:text-sm text-primary-600 font-semibold mb-1">{event.event_type}</div>
              <h3 className="text-base sm:text-lg font-semibold mb-2">{locale === 'ko' && event.name_ko ? event.name_ko : event.name}</h3>
              <p className="text-xs sm:text-sm text-gray-500 mb-2">📍 {event.location}</p>
              <p className="text-gray-600 text-xs sm:text-sm line-clamp-2">{locale === 'ko' && event.description_ko ? event.description_ko : event.description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-gray-100 py-12 sm:py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-2xl sm:text-3xl font-bold mb-3 sm:mb-4">{t('cta.title')}</h2>
          <p className="text-base sm:text-lg md:text-xl text-gray-600 mb-6 sm:mb-8 px-4">{t('cta.description')}</p>
          <Link href={`/${locale}/register`} className="btn-primary text-base sm:text-lg touch-action">
            {t('cta.button')}
          </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-6 sm:py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <p className="text-sm sm:text-base mb-2">&copy; 2025 MyLitUK. All rights reserved.</p>
            <p className="text-xs text-gray-400">
              v4.0.0 | {locale === 'ko' ? '로그인 없이 개인화 가능' : 'Personalized without login'} |
              <a href="https://mylituk-api.onrender.com/docs" target="_blank" rel="noopener noreferrer" className="ml-1 hover:text-white">
                API Docs
              </a>
            </p>
            <p className="text-xs text-gray-500 mt-1">
              {locale === 'ko'
                ? '📚 독서 리스트 | ⭐ 리뷰 | 🎯 챌린지 | 👥 커뮤니티 | 🛒 영국 서점 링크 | 📰 실시간 뉴스'
                : '📚 Reading Lists | ⭐ Reviews | 🎯 Challenges | 👥 Community | 🛒 UK Bookstores | 📰 Live News'
              }
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
