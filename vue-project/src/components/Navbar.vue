<template>
  <!-- 
    navbar 是最外層的容器。
    它的背景會是 100% 滿版寬度。
    我們在這裡加上了半透明和模糊效果，更具現代感。
  -->
  <nav class="navbar">
    <!-- 
      navbar-inner 是內容容器。
      它有最大寬度限制 (max-width)，並透過 margin: 0 auto 來水平置中。
      所有的連結、Logo 都會被限制在這個容器裡。
    -->
    <div class="navbar-inner">
      <div class="brand">
        <!-- TODO: Add your icon here -->
        <img src="" alt="Logo" style="height: 40px;"> <!-- Placeholder for the icon -->
      </div>
      
      <!-- 漢堡按鈕，只在手機版顯示 -->
      <button class="hamburger" @click="toggleMenu" :class="{ 'is-active': isMenuOpen }">
        <span></span>
        <span></span>
        <span></span>
      </button>

      <!-- 導覽連結 -->
      <ul class="nav-links" :class="{ 'nav-open': isMenuOpen }">
        <li v-for="item in items" :key="item.key">
          <a 
            :class="{ active: modelValue === item.key }" 
            href="#" 
            @click.prevent="handleLinkClick(item.key)">
            {{ item.label }}
          </a>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  modelValue: String
});

const emit = defineEmits(['update:modelValue']);

const items = [
  { key: 'main', label: '電機系介紹' },
  { key: 'curriculum_overview', label: '課程總覽' },
  { key: 'course', label: '選課系統' },
  
  
  { key: 'faculty', label: '師資' }
];

// 用來控制漢堡選單的開關狀態
const isMenuOpen = ref(false);

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

// 當點擊連結時，更新頁面並自動關閉選單
const handleLinkClick = (key) => {
  emit('update:modelValue', key);
  isMenuOpen.value = false;
};
</script>

<style scoped>
/* 主要修改點：
  1. 將背景改為帶有透明度的 RGBA 值。
  2. 增加 backdrop-filter: blur(10px) 來實現毛玻璃效果，這是現代網頁設計常用手法。
*/
.navbar {
  width: 100%;
  position: sticky;
  top: 0;
  z-index: 100;
  /* 使用帶有透明度的顏色，讓背景內容能隱約透出 */
  background: linear-gradient(90deg, rgba(79, 140, 255, 0.8) 0%, rgba(56, 201, 250, 0.8) 100%);
  /* 毛玻璃效果，讓導覽列更有質感 */
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px); /* 支援 Safari */
  color: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* 這是實現 Apple 風格的關鍵：
  - max-width 限制內容的最大寬度。
  - margin: 0 auto 讓這個容器在 navbar 內水平置中。
  - padding 確保內容不會貼著邊緣。
*/
.navbar-inner {
  max-width: none; 
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
}

.brand {
  font-size: 1.5rem;
  font-weight: 700;
}

/* 桌面版導覽連結 */
.nav-links {
  list-style: none;
  display: flex;
  margin: 0;
  padding: 0;
}

.nav-links li {
  margin-left: 28px;
}

.nav-links a {
  color: #fff;
  text-decoration: none;
  font-size: 1.1rem;
  padding: 6px 16px;
  border-radius: 20px;
  transition: background 0.2s, color 0.2s;
  white-space: nowrap; /* 防止文字換行 */
}

.nav-links a:hover {
  background: rgba(255,255,255,0.15);
}

.nav-links a.active {
  background: #fff;
  color: #4f8cff;
  font-weight: bold;
}

/* 漢堡按鈕樣式 (保持不變) */
.hamburger {
  display: none;
  flex-direction: column;
  justify-content: space-around;
  width: 2rem;
  height: 2rem;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 10;
}

.hamburger span {
  width: 2rem;
  height: 0.25rem;
  background: #fff;
  border-radius: 10px;
  transition: all 0.3s linear;
  position: relative;
  transform-origin: 1px;
}

.hamburger.is-active span:nth-child(1) {
  transform: rotate(45deg);
}
.hamburger.is-active span:nth-child(2) {
  opacity: 0;
  transform: translateX(20px);
}
.hamburger.is-active span:nth-child(3) {
  transform: rotate(-45deg);
}
</style>

/* --- 響應式設計：當螢幕寬度小於 768px 時 --- */
@media (max-width: 768px) {
  .nav-links {
    display: none;
    flex-direction: column;
    width: 100%;
    position: absolute;
    top: 100%; /* 改為 100% 讓它緊貼著 navbar-inner 的下方 */
    left: 0;
    /* 確保下拉選單的背景也有一致的模糊效果 */
    background: rgba(67, 158, 253, 0.85);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    padding: 1rem 0;
  }

  .nav-links.nav-open {
    display: flex;
  }

  .nav-links li {
    margin: 0;
    text-align: center;
  }
  
  .nav-links a {
    display: block;
    padding: 1rem;
    border-radius: 0;
  }

  .hamburger {
    display: flex;
  }
}
