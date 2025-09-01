<template>
  <!-- 根據視窗大小和使用者偏好選擇顯示側邊欄或頂部導航 -->
  <div :class="['navbar-container', { 'sidebar': isSidebarOpen, 'topbar': !isSidebarOpen }]">
    <!-- 側邊欄模式 -->
    <aside v-if="isSidebarOpen" class="sidebar-nav">
      <!-- 側邊欄標頭 -->
      <div class="sidebar-header">
        <div class="brand">
          <img src="/favicon.ico" alt="MCU EE" class="brand-icon">
          <span class="brand-text">MCU 電機系</span>
        </div>
        <!-- 僅在移動版顯示關閉側邊欄按鈕 -->
        <button class="close-sidebar-btn" @click="$emit('toggle-sidebar')" aria-label="關閉側欄">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- 側邊欄菜單項目 -->
      <nav class="sidebar-menu">
        <ul class="menu-items">
          <li v-for="item in items" :key="item.key" class="menu-item">
            <a 
              :class="['menu-link', { active: modelValue === item.key }]"
              href="#" 
              @click.prevent="handleLinkClick(item.key)"
            >
              <svg-icon :name="item.icon" class="menu-icon" />
              <span>{{ item.label }}</span>
            </a>
          </li>
        </ul>
      </nav>

      <!-- 側邊欄底部工具區 -->
      <div class="sidebar-footer">
        <!-- 深淺色切換按鈕 -->
        <button @click="$emit('toggle-dark-mode')" class="theme-toggle-btn" :aria-label="isDark ? '切換至淺色模式' : '切換至深色模式'">
          <svg v-if="isDark" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
          </svg>
          <span class="ml-2">{{ isDark ? '淺色模式' : '深色模式' }}</span>
        </button>
      </div>
    </aside>

    <!-- 頂部導航模式 -->
    <nav v-else class="topbar-nav">
      <div class="topbar-inner">
        <!-- 左側：漢堡選單按鈕 + Logo -->
        <div class="topbar-left">
          <button class="hamburger" @click="$emit('toggle-sidebar')" aria-label="開啟選單">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <div class="brand">
            <img src="/favicon.ico" alt="MCU EE" class="brand-icon">
            <span class="brand-text">MCU 電機系</span>
          </div>
        </div>

        <!-- 中間：導航連結 (在非移動設備上顯示) -->
        <ul class="nav-links">
          <li v-for="item in items" :key="item.key">
            <a 
              :class="{ active: modelValue === item.key }" 
              href="#" 
              @click.prevent="handleLinkClick(item.key)"
            >
              {{ item.label }}
            </a>
          </li>
        </ul>

        <!-- 右側：主題切換按鈕 -->
        <div class="topbar-right">
          <button @click="$emit('toggle-dark-mode')" class="theme-toggle-btn" :aria-label="isDark ? '切換至淺色模式' : '切換至深色模式'">
            <svg v-if="isDark" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          </button>
        </div>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  modelValue: String,
  isSidebarOpen: Boolean,
  isDark: Boolean
});

const emit = defineEmits(['update:modelValue', 'toggle-sidebar', 'toggle-dark-mode']);

// 使用SVG圖示的選單項目
const items = [
  { key: 'main', label: '電機系介紹', icon: 'home' },
  { key: 'curriculum_overview', label: '課程總覽', icon: 'book' },
  { key: 'course', label: '選課系統', icon: 'calendar' },
  { key: 'faculty', label: '師資陣容', icon: 'users' }
];

// SVG 圖示元件
const SvgIcon = {
  props: {
    name: String
  },
  setup(props) {
    // 不同圖示的SVG路徑
    const icons = {
      home: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6',
      book: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253',
      calendar: 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z',
      users: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z'
    };

    // 返回對應的SVG路徑
    const path = computed(() => {
      return icons[props.name] || '';
    });

    return { path };
  },
  template: `
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="svg-icon">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="path" />
    </svg>
  `
};

// 當點擊連結時，更新頁面
const handleLinkClick = (key) => {
  emit('update:modelValue', key);
};
</script>

<style scoped>
/* 共享樣式 */
.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 600;
}

.brand-icon {
  height: 32px;
  width: 32px;
  border-radius: 6px;
  object-fit: cover;
}

.brand-text {
  font-size: 1.25rem;
  font-family: 'Noto Sans TC', sans-serif;
  font-weight: 600;
  white-space: nowrap;
}

.svg-icon {
  width: 1.25rem;
  height: 1.25rem;
}

/* 側邊欄樣式 */
.sidebar {
  width: 250px;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  background-color: var(--bg-card);
  border-right: 1px solid var(--border-color);
  box-shadow: var(--shadow-md);
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1rem;
  border-bottom: 1px solid var(--border-color);
}

.sidebar-menu {
  flex: 1;
  overflow-y: auto;
  padding: 1rem 0;
}

.menu-items {
  list-style: none;
  padding: 0;
  margin: 0;
}

.menu-item {
  margin-bottom: 0.5rem;
}

.menu-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  color: var(--text-primary);
  padding: 0.75rem 1rem;
  transition: all 0.2s ease;
  border-radius: 0.5rem;
  margin: 0 0.5rem;
}

.menu-link:hover {
  background-color: rgba(var(--primary-rgb), 0.08);
}

.menu-link.active {
  background: linear-gradient(90deg, var(--primary), var(--primary-dark));
  color: white;
}

.menu-icon {
  width: 1.25rem;
  height: 1.25rem;
  transition: all 0.2s ease;
}

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid var(--border-color);
}

.close-sidebar-btn {
  background: transparent;
  border: none;
  color: var(--text-primary);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.5rem;
  transition: all 0.2s ease;
}

.close-sidebar-btn:hover {
  background-color: rgba(var(--primary-rgb), 0.08);
}

/* 頂部導航樣式 */
.topbar {
  width: 100%;
}

.topbar-nav {
  position: sticky;
  top: 0;
  z-index: 100;
  width: 100%;
  background-color: var(--bg-card);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: var(--shadow-sm);
  border-bottom: 1px solid var(--border-color);
}

.topbar-inner {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  position: relative;
}

.topbar-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* 漢堡選單按鈕 */
.hamburger {
  background: transparent;
  border: none;
  color: var(--text-primary);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.hamburger:hover {
  background-color: rgba(var(--primary-rgb), 0.08);
}

/* 導航連結 */
.nav-links {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 1.5rem;
}

.nav-links a {
  color: var(--text-primary);
  text-decoration: none;
  font-size: 1rem;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  transition: all 0.2s ease;
}

.nav-links a:hover {
  background-color: rgba(var(--primary-rgb), 0.08);
}

.nav-links a.active {
  background: linear-gradient(90deg, var(--primary), var(--primary-dark));
  color: white;
}

/* 主題切換按鈕 */
.theme-toggle-btn {
  background: transparent;
  border: none;
  color: var(--text-primary);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.theme-toggle-btn:hover {
  background-color: rgba(var(--primary-rgb), 0.08);
}

/* 響應式設計 */
@media (max-width: 1024px) {
  .sidebar {
    transform: translateX(-100%);
    box-shadow: none;
  }

  .sidebar.sidebar-open {
    transform: translateX(0);
    box-shadow: var(--shadow-lg);
  }
}

@media (max-width: 768px) {
  .nav-links {
    display: none;
  }
}
</style>
