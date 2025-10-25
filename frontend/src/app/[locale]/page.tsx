'use client';

import { useTranslations } from 'next-intl';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function HomePage() {
  const t = useTranslations('home');
  const tCommon = useTranslations('common');
  const tNav = useTranslations('nav');
  const params = useParams();
  const locale = params.locale as string;

  const [authors, setAuthors] = useState([]);
  const [books, setBooks] = useState([]);
  const [events, setEvents] = useState([]);

  useEffect(() => {
    // 작가 목록 가져오기
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/authors?size=3`)
      .then(res => res.json())
      .then(data => setAuthors(data.items || []))
      .catch(err => console.log(err));

    // 책 목록 가져오기
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/books/new?size=3`)
      .then(res => res.json())
      .then(data => setBooks(data.items || []))
      .catch(err => console.log(err));

    // 이벤트 목록 가져오기
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/events?upcoming=true&size=3`)
      .then(res => res.json())
      .then(data => setEvents(data.items || []))
      .catch(err => console.log(err));
  }, []);

  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-primary-600">{t('title')}</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Link href={`/${locale}/login`} className="text-gray-700 hover:text-primary-600">
                {tNav('login')}
              </Link>
              <Link href={`/${locale}/register`} className="btn-primary">
                {tNav('register')}
              </Link>
              <select
                value={locale}
                onChange={(e) => {
                  const newLocale = e.target.value;
                  window.location.href = `/${newLocale}`;
                }}
                className="px-3 py-1 border border-gray-300 rounded-md"
              >
                <option value="en">English</option>
                <option value="ko">한국어</option>
              </select>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-5xl font-bold mb-4">{t('subtitle')}</h1>
            <p className="text-xl mb-8 max-w-3xl mx-auto">{t('description')}</p>
            <Link href={`/${locale}/register`} className="inline-block bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
              {t('cta.button')}
            </Link>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 className="text-3xl font-bold text-center mb-12">{t('features.title')}</h2>
        <div className="grid md:grid-cols-3 gap-8">
          <div className="card text-center">
            <div className="text-4xl mb-4">📚</div>
            <h3 className="text-xl font-semibold mb-2">{t('features.personalized.title')}</h3>
            <p className="text-gray-600">{t('features.personalized.description')}</p>
          </div>
          <div className="card text-center">
            <div className="text-4xl mb-4">🔔</div>
            <h3 className="text-xl font-semibold mb-2">{t('features.alerts.title')}</h3>
            <p className="text-gray-600">{t('features.alerts.description')}</p>
          </div>
          <div className="card text-center">
            <div className="text-4xl mb-4">🌐</div>
            <h3 className="text-xl font-semibold mb-2">{t('features.multilingual.title')}</h3>
            <p className="text-gray-600">{t('features.multilingual.description')}</p>
          </div>
        </div>
      </div>

      {/* Authors Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 className="text-3xl font-bold mb-8">Featured UK Authors</h2>
        <div className="grid md:grid-cols-3 gap-6">
          {authors.map((author: any) => (
            <div key={author.id} className="card">
              <h3 className="text-xl font-semibold mb-2">{locale === 'ko' && author.name_ko ? author.name_ko : author.name}</h3>
              <p className="text-gray-600 text-sm line-clamp-3">{locale === 'ko' && author.bio_ko ? author.bio_ko : author.bio}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Books Section */}
      <div className="bg-gray-50 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold mb-8">Latest Books</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {books.map((book: any) => (
              <div key={book.id} className="card">
                <h3 className="text-lg font-semibold mb-2">{locale === 'ko' && book.title_ko ? book.title_ko : book.title}</h3>
                <p className="text-sm text-gray-500 mb-2">by {book.author_name}</p>
                <p className="text-gray-600 text-sm line-clamp-2">{locale === 'ko' && book.description_ko ? book.description_ko : book.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Events Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 className="text-3xl font-bold mb-8">Upcoming Events</h2>
        <div className="grid md:grid-cols-3 gap-6">
          {events.map((event: any) => (
            <div key={event.id} className="card">
              <div className="text-sm text-primary-600 font-semibold mb-1">{event.event_type}</div>
              <h3 className="text-lg font-semibold mb-2">{locale === 'ko' && event.name_ko ? event.name_ko : event.name}</h3>
              <p className="text-sm text-gray-500 mb-2">📍 {event.location}</p>
              <p className="text-gray-600 text-sm line-clamp-2">{locale === 'ko' && event.description_ko ? event.description_ko : event.description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-gray-100 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-4">{t('cta.title')}</h2>
          <p className="text-xl text-gray-600 mb-8">{t('cta.description')}</p>
          <Link href={`/${locale}/register`} className="btn-primary text-lg">
            {t('cta.button')}
          </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p>&copy; 2025 MyLitUK. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
