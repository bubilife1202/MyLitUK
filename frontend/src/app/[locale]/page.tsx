'use client';

import { useTranslations } from 'next-intl';
import Link from 'next/link';
import { useParams } from 'next/navigation';

export default function HomePage() {
  const t = useTranslations('home');
  const tCommon = useTranslations('common');
  const tNav = useTranslations('nav');
  const params = useParams();
  const locale = params.locale as string;

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
