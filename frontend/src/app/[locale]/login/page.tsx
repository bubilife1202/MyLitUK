'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { authApi } from '@/lib/api';
import { useAuthStore } from '@/store/authStore';

export default function LoginPage() {
  const t = useTranslations('auth.login');
  const tCommon = useTranslations('common');
  const router = useRouter();
  const params = useParams();
  const locale = params.locale as string;
  const setUser = useAuthStore((state) => state.setUser);

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await authApi.login(email, password);
      const { access_token } = response.data;

      localStorage.setItem('access_token', access_token);

      // Get user info
      const userResponse = await authApi.getMe();
      setUser(userResponse.data);

      router.push(`/${locale}/dashboard`);
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
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
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
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="input mt-1"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full btn-primary"
          >
            {loading ? tCommon('loading') : t('submit')}
          </button>

          <div className="text-center text-sm">
            <span className="text-gray-600">{t('noAccount')} </span>
            <Link href={`/${locale}/register`} className="text-primary-600 hover:text-primary-700">
              {t('signUp')}
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
