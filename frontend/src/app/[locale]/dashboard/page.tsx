'use client';

import { useEffect, useState } from 'react';
import { useTranslations } from 'next-intl';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { dashboardApi } from '@/lib/api';
import { useAuthStore } from '@/store/authStore';

export default function DashboardPage() {
  const t = useTranslations('dashboard');
  const tCommon = useTranslations('common');
  const tNav = useTranslations('nav');
  const router = useRouter();
  const params = useParams();
  const locale = params.locale as string;
  const { isAuthenticated, user, logout } = useAuthStore();

  const [dashboard, setDashboard] = useState<any>(null);
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!isAuthenticated) {
      router.push(`/${locale}/login`);
      return;
    }

    loadDashboard();
    loadStats();
  }, [isAuthenticated]);

  const loadDashboard = async () => {
    try {
      const response = await dashboardApi.get();
      setDashboard(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || tCommon('error'));
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/dashboard/stats`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setStats(data);
      }
    } catch (err) {
      console.error('Failed to load stats:', err);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">{tCommon('loading')}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center space-x-8">
              <Link href={`/${locale}`}>
                <h1 className="text-2xl font-bold text-primary-600">MyLitUK</h1>
              </Link>
              <div className="flex space-x-4">
                <Link href={`/${locale}/dashboard`} className="text-primary-600 font-semibold">
                  {tNav('dashboard')}
                </Link>
                <Link href={`/${locale}/my-books`} className="text-gray-700 hover:text-primary-600">
                  My Books
                </Link>
                <Link href={`/${locale}/authors`} className="text-gray-700 hover:text-primary-600">
                  {tNav('authors')}
                </Link>
                <Link href={`/${locale}/events`} className="text-gray-700 hover:text-primary-600">
                  {tNav('events')}
                </Link>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Link href={`/${locale}/notifications`} className="text-gray-700 hover:text-primary-600">
                {tNav('notifications')}
              </Link>
              <span className="text-gray-700">{user?.username}</span>
              <button onClick={logout} className="text-gray-700 hover:text-primary-600">
                {tNav('logout')}
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Dashboard Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold mb-2">{t('title')}</h1>
        <p className="text-gray-600 mb-8">{t('welcome')}</p>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {/* Reading Stats */}
        {stats && stats.reading_stats && (
          <div className="mb-8">
            <h2 className="text-2xl font-bold mb-4">My Reading</h2>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              <div className="card text-center">
                <div className="text-3xl font-bold text-blue-600">{stats.reading_stats.want_to_read}</div>
                <div className="text-sm text-gray-600">Want to Read</div>
              </div>
              <div className="card text-center">
                <div className="text-3xl font-bold text-yellow-600">{stats.reading_stats.reading}</div>
                <div className="text-sm text-gray-600">Currently Reading</div>
              </div>
              <div className="card text-center">
                <div className="text-3xl font-bold text-green-600">{stats.reading_stats.finished}</div>
                <div className="text-sm text-gray-600">Finished</div>
              </div>
              <div className="card text-center">
                <div className="text-3xl font-bold text-red-600">{stats.reading_stats.favorites}</div>
                <div className="text-sm text-gray-600">Favorites</div>
              </div>
              <div className="card text-center">
                <div className="text-3xl font-bold text-purple-600">{stats.review_stats.total_reviews}</div>
                <div className="text-sm text-gray-600">Reviews</div>
              </div>
            </div>
          </div>
        )}

        {/* Reading Challenge */}
        {stats && stats.challenge_stats && stats.challenge_stats.goal && (
          <div className="card mb-8">
            <h2 className="text-xl font-bold mb-4">📚 Reading Challenge {new Date().getFullYear()}</h2>
            <div className="mb-2">
              <div className="flex justify-between text-sm mb-1">
                <span>{stats.challenge_stats.current} of {stats.challenge_stats.goal} books</span>
                <span>{stats.challenge_stats.percentage}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-4">
                <div
                  className="bg-primary-600 h-4 rounded-full transition-all"
                  style={{width: `${Math.min(stats.challenge_stats.percentage, 100)}%`}}
                ></div>
              </div>
            </div>
          </div>
        )}

        {/* Summary Cards */}
        {dashboard && (
          <>
            <h2 className="text-2xl font-bold mb-4">Following</h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              <div className="card">
                <div className="text-3xl font-bold text-primary-600">{dashboard.summary.followed_authors}</div>
                <div className="text-gray-600">{t('summary.followedAuthors')}</div>
              </div>
              <div className="card">
                <div className="text-3xl font-bold text-primary-600">{dashboard.summary.followed_events}</div>
                <div className="text-gray-600">{t('summary.followedEvents')}</div>
              </div>
              <div className="card">
                <div className="text-3xl font-bold text-primary-600">{dashboard.summary.followed_awards}</div>
                <div className="text-gray-600">{t('summary.followedAwards')}</div>
              </div>
              <div className="card">
                <div className="text-3xl font-bold text-primary-600">{dashboard.summary.unread_notifications}</div>
                <div className="text-gray-600">{t('summary.unreadNotifications')}</div>
              </div>
            </div>

            {/* New Books */}
            <div className="card mb-8">
              <h2 className="text-2xl font-bold mb-4">{t('newBooks.title')}</h2>
              {dashboard.new_books.length === 0 ? (
                <p className="text-gray-600">{t('newBooks.empty')}</p>
              ) : (
                <div className="space-y-4">
                  {dashboard.new_books.map((book: any) => (
                    <div key={book.book_id} className="border-b pb-4 last:border-b-0">
                      <h3 className="font-semibold text-lg">{book.title}</h3>
                      <p className="text-gray-600">by {book.author_name}</p>
                      {book.publication_date && (
                        <p className="text-sm text-gray-500">Publication: {book.publication_date}</p>
                      )}
                      {book.amazon_url && (
                        <a href={book.amazon_url} target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:underline text-sm">
                          View on Amazon
                        </a>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Upcoming Events */}
            <div className="card mb-8">
              <h2 className="text-2xl font-bold mb-4">{t('upcomingEvents.title')}</h2>
              {dashboard.upcoming_events.length === 0 ? (
                <p className="text-gray-600">{t('upcomingEvents.empty')}</p>
              ) : (
                <div className="space-y-4">
                  {dashboard.upcoming_events.map((event: any) => (
                    <div key={event.event_id} className="border-b pb-4 last:border-b-0">
                      <h3 className="font-semibold text-lg">{event.name}</h3>
                      <p className="text-gray-600">{event.city}, {event.region}</p>
                      <p className="text-sm text-gray-500">
                        {event.start_date} to {event.end_date}
                      </p>
                      {event.ticket_url && (
                        <a href={event.ticket_url} target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:underline text-sm">
                          Get Tickets
                        </a>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Award Updates */}
            <div className="card mb-8">
              <h2 className="text-2xl font-bold mb-4">{t('awardUpdates.title')}</h2>
              {dashboard.award_updates.length === 0 ? (
                <p className="text-gray-600">{t('awardUpdates.empty')}</p>
              ) : (
                <div className="space-y-4">
                  {dashboard.award_updates.map((award: any, index: number) => (
                    <div key={index} className="border-b pb-4 last:border-b-0">
                      <h3 className="font-semibold text-lg">{award.award_name}</h3>
                      <p className="text-gray-600">{award.year} - {award.stage}</p>
                      {award.announcement_date && (
                        <p className="text-sm text-gray-500">Announcement: {award.announcement_date}</p>
                      )}
                      {award.announced && (
                        <span className="badge-success">Announced</span>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
