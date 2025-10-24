# 사이트 내 알림 시스템 & 재방문 유도 전략

## 🎯 핵심 목표
**이메일 없이 사용자가 사이트에 계속 방문하도록 만들기**

---

## 📢 사이트 내 알림 시스템 (In-App Notifications)

### 1. 알림 센터 (Notification Center)

#### UI 구조
```
┌─────────────────────────────────────────┐
│  Header                          [🔔 3]  │ ← 읽지 않은 알림 배지
└─────────────────────────────────────────┘
                ↓ 클릭
┌─────────────────────────────────────────┐
│  알림                          [모두읽음] │
├─────────────────────────────────────────┤
│ 🎉 Booker Prize 수상작 발표!            │
│    "Prophet Song" Paul Lynch            │
│    [지금 구매하기]            5분 전 ●   │
├─────────────────────────────────────────┤
│ 🎫 Hay Festival 티켓 오픈 1시간 전!     │
│    [티켓 구매]                2시간 전   │
├─────────────────────────────────────────┤
│ 📚 Ian McEwan 신간 출시                  │
│    "Lessons" 출시되었습니다              │
│    [상세보기]                  1일 전    │
└─────────────────────────────────────────┘
```

#### 알림 타입별 디자인
```javascript
// 우선순위별 시각적 차별화
const notificationStyles = {
  HIGH: {
    // 문학상 Winner, 티켓 오픈 임박
    icon: "🎉",
    color: "bg-red-500",
    badge: true,
    sound: true
  },
  MEDIUM: {
    // Shortlist, 신간 출시
    icon: "📚",
    color: "bg-blue-500",
    badge: true,
    sound: false
  },
  LOW: {
    // 새 행사 등록, Longlist
    icon: "ℹ️",
    color: "bg-gray-500",
    badge: false,
    sound: false
  }
}
```

---

## 🏠 개인화된 대시보드 (Personalized Dashboard)

### "For You" 피드

#### 1. 최신 알림 요약
```
┌─────────────────────────────────────────┐
│  오늘의 업데이트 (3)                     │
├─────────────────────────────────────────┤
│  📚 신간 2건                             │
│  🎭 다가오는 행사 1건                    │
│  🏆 문학상 발표 예정 1건                 │
└─────────────────────────────────────────┘
```

#### 2. 개인화된 타임라인
```
┌─────────────────────────────────────────┐
│  이번 주 놓치면 안 될 일정               │
├─────────────────────────────────────────┤
│  [오늘]                                  │
│  • Booker Prize Shortlist 발표          │
│                                          │
│  [내일]                                  │
│  • Zadie Smith 신간 출시                │
│                                          │
│  [이번 주 토요일]                        │
│  • 런던 시 낭독회 (Poetry Reading)       │
│    [티켓 구매] [관심 없음]               │
└─────────────────────────────────────────┘
```

#### 3. 맞춤 추천
```
┌─────────────────────────────────────────┐
│  회원님이 좋아할 만한 콘텐츠             │
├─────────────────────────────────────────┤
│  📖 Hilary Mantel의 새 전기 출간         │
│  🎭 맨체스터 Crime 페스티벌 라인업 공개  │
│  🏆 Women's Prize Longlist 13권 확인     │
└─────────────────────────────────────────┘
```

---

## 🔔 실시간 알림 시스템

### 기술 구현

#### 1. WebSocket 연결 (실시간)
```javascript
// Frontend: 실시간 알림 수신
const socket = new WebSocket('wss://mylituk.com/notifications');

socket.onmessage = (event) => {
  const notification = JSON.parse(event.data);

  // 토스트 알림 표시
  showToast({
    title: notification.title,
    message: notification.message,
    type: notification.priority
  });

  // 배지 카운트 업데이트
  updateBadgeCount();
};
```

#### 2. Server-Sent Events (대안)
```python
# Backend: SSE로 알림 푸시
from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse

@app.get("/api/notifications/stream")
async def notification_stream(user_id: int):
    async def event_generator():
        while True:
            # 새 알림 체크
            new_notifications = await get_new_notifications(user_id)
            if new_notifications:
                yield {
                    "event": "notification",
                    "data": json.dumps(new_notifications)
                }
            await asyncio.sleep(30)  # 30초마다 체크

    return EventSourceResponse(event_generator())
```

#### 3. Polling (가장 간단, MVP용)
```javascript
// 30초마다 새 알림 체크
setInterval(async () => {
  const response = await fetch('/api/notifications/unread');
  const { count, notifications } = await response.json();

  if (count > 0) {
    updateBadge(count);
    showNewNotifications(notifications);
  }
}, 30000);
```

---

## 🎮 사용자 재방문 유도 전략

### 1. 읽지 않은 알림 배지 (핵심!)
```
헤더에 항상 표시:
🔔 [3]  ← 빨간 배지로 시각적 자극

심리적 효과:
- "3개의 읽지 않은 알림" → 확인하고 싶은 욕구
- 숫자가 0이 될 때까지 방문 유도
```

### 2. 일일 방문 보상
```
┌─────────────────────────────────────────┐
│  연속 방문 7일째! 🔥                     │
│  ████████░░░░░░  (10일 목표)            │
│                                          │
│  보상: 프리미엄 콘텐츠 1개 무료 열람     │
└─────────────────────────────────────────┘
```

### 3. 개인화된 주간 리포트
```
┌─────────────────────────────────────────┐
│  이번 주 당신의 문학 생활               │
├─────────────────────────────────────────┤
│  📊 새 알림 12개 확인                    │
│  📚 관심 신간 3권 출시                   │
│  🎭 다가오는 행사 2건                    │
│  🏆 팔로우 중인 문학상 발표 1건          │
│                                          │
│  [상세보기]                              │
└─────────────────────────────────────────┘
```

### 4. "오늘의 하이라이트"
```
매일 바뀌는 콘텐츠로 신선함 유지:

월요일: "이번 주 출시 예정 신간 Top 5"
화요일: "오늘의 문학 뉴스"
수요일: "다가오는 행사 스포트라이트"
목요일: "주목할 만한 신인 작가"
금요일: "주말에 읽을 책 추천"
```

### 5. 카운트다운 타이머
```
┌─────────────────────────────────────────┐
│  🎫 Hay Festival 티켓 오픈까지           │
│                                          │
│     2일 15시간 32분                      │
│                                          │
│  [알림 설정됨 ✓]                         │
└─────────────────────────────────────────┘
```

---

## 📊 데이터베이스 스키마 수정

### 기존 notifications 테이블 유지
```sql
-- 이메일 관련 필드만 제거/무시
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(300) NOT NULL,
    message TEXT NOT NULL,
    related_id INTEGER,
    related_type VARCHAR(50),
    action_url VARCHAR(500),
    priority VARCHAR(20) DEFAULT 'medium',  -- 'high', 'medium', 'low'
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 인덱스 추가 (빠른 조회)
CREATE INDEX idx_notifications_user_unread
    ON notifications(user_id, is_read, created_at DESC);
```

### 새로운 테이블: 사용자 활동 추적
```sql
-- 사용자 방문 기록 (재방문 유도용)
CREATE TABLE user_visit_streaks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    visit_date DATE NOT NULL,
    streak_count INTEGER DEFAULT 1,
    UNIQUE(user_id, visit_date)
);

-- 알림 읽음 통계
CREATE TABLE notification_stats (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    total_notifications INTEGER DEFAULT 0,
    read_notifications INTEGER DEFAULT 0,
    last_visit TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔔 API 엔드포인트 수정

### 알림 관련 API (변경 없음, 추가만)
```
GET    /api/notifications              # 알림 목록
GET    /api/notifications/unread       # 안 읽은 알림
GET    /api/notifications/count        # 안 읽은 개수만
PUT    /api/notifications/:id/read     # 읽음 처리
PUT    /api/notifications/mark-all-read # 모두 읽음
DELETE /api/notifications/:id          # 삭제
GET    /api/notifications/stream       # 실시간 SSE (NEW)
```

### 대시보드 API (NEW)
```
GET    /api/dashboard/today            # 오늘의 업데이트
GET    /api/dashboard/timeline         # 개인화 타임라인
GET    /api/dashboard/recommendations  # 맞춤 추천
GET    /api/dashboard/weekly-report    # 주간 리포트
```

### 사용자 활동 API (NEW)
```
POST   /api/user/visit                 # 방문 기록
GET    /api/user/streak                # 연속 방문 일수
GET    /api/user/stats                 # 활동 통계
```

---

## 🎨 UI/UX 주요 화면 수정

### 1. 헤더 (항상 표시)
```
┌─────────────────────────────────────────┐
│ MyLitUK  홈  행사  문학상   [🔔 3]  👤  │
│                            ↑             │
│                      읽지 않은 알림      │
└─────────────────────────────────────────┘
```

### 2. 홈 대시보드 (로그인 후)
```
┌─────────────────────────────────────────┐
│  안녕하세요, Sarah님! 👋                 │
│  오늘 새로운 소식이 3건 있습니다.        │
├─────────────────────────────────────────┤
│                                          │
│  [오늘의 업데이트] ─────────────────     │
│                                          │
│  📚 팔로우 중인 작가 신간 2건            │
│  🎭 다가오는 행사 1건                    │
│                                          │
│  [상세보기]                              │
│                                          │
├─────────────────────────────────────────┤
│                                          │
│  [이번 주 놓치면 안 될 일정] ──────       │
│                                          │
│  ⏰ 2일 후: Hay Festival 티켓 오픈       │
│  📖 4일 후: Ian McEwan 신간 출시         │
│                                          │
├─────────────────────────────────────────┤
│                                          │
│  [맞춤 추천] ─────────────────────       │
│                                          │
│  당신이 좋아할 만한 행사                 │
│  [Poetry Reading in London]              │
│                                          │
└─────────────────────────────────────────┘
```

### 3. 알림 페이지 (전용 페이지)
```
┌─────────────────────────────────────────┐
│  알림                                    │
│  [전체] [신간] [행사] [문학상]          │
├─────────────────────────────────────────┤
│                                          │
│  오늘                                    │
│  ─────────────────────────────────       │
│  🎉 Booker Prize 수상작 발표!     ●     │
│     "Prophet Song" 구매하기              │
│                                   5분 전 │
│                                          │
│  🎫 Hay Festival 티켓 오픈              │
│     [지금 구매하기]            2시간 전  │
│                                          │
│  어제                                    │
│  ─────────────────────────────────       │
│  📚 Ian McEwan 신간 출시                 │
│     [상세보기]                  어제     │
│                                          │
└─────────────────────────────────────────┘
```

---

## 🚀 재방문 유도 요소 정리

### 즉시 효과
1. **읽지 않은 알림 배지** → "확인해야 한다"는 심리
2. **실시간 업데이트** → "놓칠까봐" 자주 방문
3. **개인화된 피드** → "나만을 위한 콘텐츠"

### 습관 형성
4. **연속 방문 스트릭** → 게이미피케이션
5. **일일 하이라이트** → 매일 새로운 콘텐츠
6. **카운트다운** → 중요 날짜 전 자주 확인

### 장기 유지
7. **주간 리포트** → 정기적 리마인더
8. **맞춤 추천** → 관심사 기반 큐레이션
9. **커뮤니티 요소** → (선택적) 다른 사용자와 교류

---

## 📈 성공 지표 (KPI) 수정

### 참여도 지표
```
- 일일 활성 사용자 (DAU)
- 주간 활성 사용자 (WAU)
- 평균 세션 시간
- 페이지뷰 / 세션
- 재방문율 (Return Rate)
```

### 알림 지표
```
- 알림 읽음률 (Read Rate)
- 알림 클릭률 (CTR)
- 평균 알림 확인 시간
- 알림 → 구매 전환율
```

### 습관 형성 지표
```
- 평균 연속 방문 일수
- 7일 리텐션율
- 30일 리텐션율
- 주간 활성률
```

---

## 🔧 기술 스택 수정

### 이메일 제거, 실시간 추가
```
제거:
❌ SendGrid (이메일 서비스)
❌ Celery (이메일 발송용만 제거)

유지:
✅ Celery (알림 생성용은 유지)

추가:
✅ WebSocket or SSE (실시간 알림)
✅ Redis Pub/Sub (실시간 메시징)
```

### 실시간 알림 아키텍처
```
┌──────────────────┐
│  Celery Task     │  새 도서/행사/문학상 체크
│  (백그라운드)    │
└────────┬─────────┘
         ↓
┌────────▼─────────┐
│   알림 생성       │  DB에 notification 저장
│   (PostgreSQL)   │
└────────┬─────────┘
         ↓
┌────────▼─────────┐
│  Redis Pub/Sub   │  user_id 채널에 publish
└────────┬─────────┘
         ↓
┌────────▼─────────┐
│  WebSocket       │  연결된 클라이언트에게 푸시
│  (실시간 전송)   │
└──────────────────┘
```

---

## 💡 추가 아이디어 (선택적)

### 1. 브라우저 푸시 알림 (Progressive Web App)
```javascript
// Service Worker 등록
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js');
}

// 푸시 권한 요청
Notification.requestPermission().then(permission => {
  if (permission === 'granted') {
    // 푸시 알림 구독
  }
});
```

**장점**:
- 사이트 미방문 시에도 알림 가능
- 이메일보다 즉시성 있음
- 사용자가 직접 활성화 (opt-in)

**단점**:
- 사용자가 권한 허용해야 함
- 모바일 Safari 지원 제한적

### 2. RSS 피드 (고급 사용자용)
```xml
<!-- /api/feeds/user/:user_id/rss -->
<rss version="2.0">
  <channel>
    <title>MyLitUK - 내 알림</title>
    <item>
      <title>Booker Prize 수상작 발표</title>
      <description>Prophet Song이 수상했습니다</description>
      <pubDate>Thu, 24 Oct 2024 10:00:00 GMT</pubDate>
    </item>
  </channel>
</rss>
```

### 3. 카카오톡 알림 (한국 사용자용)
```
- 카카오톡 챗봇 연동
- 중요 알림만 카카오톡으로 발송
- 사용자가 선택적으로 연동
```

---

## ✅ 요약

### 제거된 것
- ❌ 이메일 발송 시스템
- ❌ SendGrid 등 이메일 서비스

### 새로 추가된 것
- ✅ 읽지 않은 알림 배지
- ✅ 실시간 알림 (WebSocket/SSE)
- ✅ 개인화된 대시보드
- ✅ 연속 방문 스트릭
- ✅ 오늘의 하이라이트
- ✅ 주간 리포트 (사이트 내)

### 핵심 전략
**"사이트를 방문해야만 알림을 볼 수 있다"**
→ 자연스럽게 재방문 유도!

---

**작성일**: 2025-10-24
**버전**: 2.0 (이메일 제거, 사이트 내 알림 중심)
