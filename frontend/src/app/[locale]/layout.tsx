import { NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';
import { notFound } from 'next/navigation';
import { Playfair_Display, Courier_Prime } from 'next/font/google';
import '../globals.css';

// 동적 렌더링 강제
export const dynamic = 'force-dynamic';

// Dark Academia Fonts
const playfair = Playfair_Display({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700', '800', '900'],
  variable: '--font-playfair',
  display: 'swap',
});

const courier = Courier_Prime({
  subsets: ['latin'],
  weight: ['400', '700'],
  variable: '--font-courier',
  display: 'swap',
});

export default async function LocaleLayout({
  children,
  params: { locale }
}: {
  children: React.ReactNode;
  params: { locale: string };
}) {
  const messages = await getMessages();

  if (!['en', 'ko'].includes(locale)) {
    notFound();
  }

  return (
    <html lang={locale} className={`${playfair.variable} ${courier.variable}`}>
      <body className="font-courier">
        <NextIntlClientProvider messages={messages}>
          {children}
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
