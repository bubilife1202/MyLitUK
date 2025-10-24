'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { authApi } from '@/lib/api';

export default function RegisterPage() {
  const t = useTranslations('auth.register');
  const tCommon = useTranslations('common');
  const router = useRouter();
  const params = useParams();
  const locale = params.locale as string;

  const [formData, setFormData] = useState({
    email: '',
    username: '',
    full_name: '',
    password: '',
    confirmPassword: '',
    preferred_language: locale,
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);

    try {
      const { confirmPassword, ...registerData } = formData;
      await authApi.register(registerData);
      router.push(`/${locale}/login`);
    } catch (err: any) {
      setError(err.response?.data?.detail || tCommon('error'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <Link href={`/${locale}`}>
            <h1 className="text-3xl font-bold text-primary-600">MyLitUK</h1>
          </Link>
          <h2 className="mt-6 text-2xl font-bold text-gray-900">{t('title')}</h2>
        </div>

        <form onSubmit={handleSubmit} className="card space-y-6">
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
              {t('email')}
            </label>
            <input
              id="email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              required
              className="input mt-1"
            />
          </div>

          <div>
            <label htmlFor="username" className="block text-sm font-medium text-gray-700">
              {t('username')}
            </label>
            <input
              id="username"
              name="username"
              type="text"
              value={formData.username}
              onChange={handleChange}
              required
              className="input mt-1"
            />
          </div>

          <div>
            <label htmlFor="full_name" className="block text-sm font-medium text-gray-700">
              {t('fullName')}
            </label>
            <input
              id="full_name"
              name="full_name"
              type="text"
              value={formData.full_name}
              onChange={handleChange}
              required
              className="input mt-1"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              {t('password')}
            </label>
            <input
              id="password"
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              required
              minLength={8}
              className="input mt-1"
            />
          </div>

          <div>
            <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
              {t('confirmPassword')}
            </label>
            <input
              id="confirmPassword"
              name="confirmPassword"
              type="password"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
              minLength={8}
              className="input mt-1"
            />
          </div>

          <div>
            <label htmlFor="preferred_language" className="block text-sm font-medium text-gray-700">
              {t('preferredLanguage')}
            </label>
            <select
              id="preferred_language"
              name="preferred_language"
              value={formData.preferred_language}
              onChange={handleChange}
              className="input mt-1"
            >
              <option value="en">English</option>
              <option value="ko">한국어</option>
            </select>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full btn-primary"
          >
            {loading ? tCommon('loading') : t('submit')}
          </button>

          <div className="text-center text-sm">
            <span className="text-gray-600">{t('haveAccount')} </span>
            <Link href={`/${locale}/login`} className="text-primary-600 hover:text-primary-700">
              {t('signIn')}
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
