<script setup>
import { ref, computed, onMounted } from 'vue';
import Navbar from './components/Navbar.vue';
import MainScreen from './components/MainScreen.vue';
import CourseSelection from './components/CourseSelection.vue';
import CourseCurriculum from './components/CourseCurriculum.vue';
import Faculty from './components/Faculty.vue';
import useDarkMode from './composables/useDarkMode';

const page = ref('main');
const isSidebarOpen = ref(window.innerWidth > 768); // 在大螢幕預設打開
const { isDark, toggleDarkMode } = useDarkMode();

// 是否在電腦版顯示為兩欄式佈局
const isDesktopLayout = computed(() => {
  return page.value === 'course' && window.innerWidth > 1024;
});

// 處理視窗大小變化
const handleResize = () => {
  isSidebarOpen.value = window.innerWidth > 768;
};

onMounted(() => {
  window.addEventListener('resize', handleResize);
});
</script>

<template>
  <div id="app" :class="{ 'dark': isDark }">
    <div class="app-container" :class="{ 'is-desktop-layout': isDesktopLayout }">
      <!-- Navbar 在側邊或頂部 -->
      <Navbar 
        v-model="page" 
        :is-sidebar-open="isSidebarOpen" 
        @toggle-sidebar="isSidebarOpen = !isSidebarOpen"
        @toggle-dark-mode="toggleDarkMode"
        :is-dark="isDark"
      />

      <!-- 主要內容區 -->
      <main :class="['content', { 'sidebar-open': isSidebarOpen, 'content-expanded': !isSidebarOpen }]">
        <div v-if="page === 'main'" class="main-center">
          <MainScreen @navigate="page = $event" />
        </div>
        <div v-else-if="isDesktopLayout" class="desktop-layout">
          <!-- 電腦版兩欄式佈局 -->
          <CourseSelection />
        </div>
        <div v-else>
          <CourseSelection v-if="page === 'course'" />
          <CourseCurriculum v-else-if="page === 'curriculum_overview'" />
          <Faculty v-else-if="page === 'faculty'" />
        </div>
      </main>
    </div>
  </div>
</template>

<style>
/* 全局變量 */
:root {
  --primary: #4361ee;
  --primary-dark: #3a0ca3;
  --secondary: #4cc9f0;
  --text-primary: #333333;
  --text-secondary: #555555;
  --bg-light: #f8f9fc;
  --bg-card: #ffffff;
  --border-color: rgba(229, 231, 235, 0.5);
  --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.06);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --primary-rgb: 67, 97, 238;
  --primary-dark-rgb: 58, 12, 163;
  --secondary-rgb: 76, 201, 240;
}

/* 暗色模式變量 */
.dark {
  --primary: #7b89f4;
  --primary-dark: #6246ea;
  --secondary: #52d3ff;
  --text-primary: #e2e8f0;
  --text-secondary: #cbd5e1;
  --bg-light: #1a202c;
  --bg-card: #2d3748;
  --border-color: rgba(75, 85, 99, 0.5);
  --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.4), 0 4px 6px -2px rgba(0, 0, 0, 0.2);
  --primary-rgb: 123, 137, 244;
  --primary-dark-rgb: 98, 70, 234;
  --secondary-rgb: 82, 211, 255;
}

/* 基本樣式 */
body {
  margin: 0;
  font-family: 'Inter', 'Noto Sans TC', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
  background-color: var(--bg-light);
  color: var(--text-primary);
  line-height: 1.6;
  transition: background-color 0.3s ease, color 0.3s ease;
}

#app {
  min-height: 100vh;
}

.app-container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 主要內容區 */
.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 2rem;
  position: relative;
  z-index: 1;
  transition: all 0.3s ease;
  margin-left: 0;
}

.main-center {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 側邊欄打開的樣式 */
.content.sidebar-open {
  margin-left: 250px;
  width: calc(100% - 250px);
}

/* 桌面布局 */
.desktop-layout {
  display: flex;
  gap: 1.5rem;
}

/* 兩欄式佈局 */
.is-desktop-layout .content {
  padding: 0;
}

/* 響應式調整 */
@media (max-width: 1024px) {
  .content.sidebar-open {
    margin-left: 0;
    width: 100%;
  }
}

@media (max-width: 768px) {
  .content {
    padding: 1rem 0.75rem;
  }
}

/* 定義全域的卡片樣式 */
.card {
  background-color: var(--bg-card);
  border-radius: 0.75rem;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: var(--shadow-lg);
}

/* 動畫 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* 按鈕樣式 */
button {
  transition: all 0.3s ease;
}
</style>
