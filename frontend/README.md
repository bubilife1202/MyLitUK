# MyLitUK Frontend

Next.js 14 frontend with multilingual support (English/Korean) for the MyLitUK platform.

## Features

- Next.js 14 with App Router
- TypeScript
- Tailwind CSS
- next-intl for internationalization (English/Korean)
- Zustand for state management
- Axios for API requests

## Getting Started

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set `NEXT_PUBLIC_API_URL` to your backend URL.

3. **Run development server**:
   ```bash
   npm run dev
   ```

4. **Open browser**:
   Navigate to [http://localhost:3000](http://localhost:3000) or [http://localhost:3000/ko](http://localhost:3000/ko) for Korean.

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── [locale]/          # Locale-based routing
│   │   │   ├── page.tsx       # Home page
│   │   │   ├── login/         # Login page
│   │   │   ├── register/      # Register page
│   │   │   ├── dashboard/     # Dashboard page
│   │   │   └── layout.tsx     # Layout with i18n
│   │   └── globals.css        # Global styles
│   ├── lib/
│   │   └── api.ts             # API client
│   ├── store/
│   │   └── authStore.ts       # Auth state management
│   ├── i18n.ts                # i18n configuration
│   └── middleware.ts          # Next.js middleware for i18n
├── messages/
│   ├── en.json                # English translations
│   └── ko.json                # Korean translations
└── package.json
```

## Pages

- `/` - Home page with features and CTA
- `/login` - Login page
- `/register` - Registration page
- `/dashboard` - Personalized dashboard (requires authentication)
  - Shows new books from followed authors
  - Shows upcoming events from followed events
  - Shows award updates from followed awards

## Multilingual Support

The app supports English and Korean. Users can switch languages using the language selector in the navigation.

Routes:
- English: `/en/*`
- Korean: `/ko/*`

## Building for Production

```bash
npm run build
npm start
```

## Deployment

### Vercel (Recommended)

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Deploy:
   ```bash
   vercel
   ```

3. Set environment variable in Vercel dashboard:
   - `NEXT_PUBLIC_API_URL`: Your backend API URL

## API Integration

The frontend communicates with the FastAPI backend through the API client (`src/lib/api.ts`). All API endpoints are defined there:

- `authApi`: Authentication (login, register, me)
- `authorsApi`: Authors listing and follow/unfollow
- `eventsApi`: Events listing and follow/unfollow
- `awardsApi`: Awards listing and follow/unfollow
- `notificationsApi`: Notifications management
- `dashboardApi`: Personalized dashboard data

## License

MIT
