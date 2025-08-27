

<template>
  <nav class="navbar">
    <div class="navbar-inner">
      <div class="brand">銘傳大學選課系統</div>
      <ul class="nav-links">
        <li v-for="item in items" :key="item.key">
          <a :class="{active: modelValue === item.key}" href="#" @click.prevent="$emit('update:modelValue', item.key)">
            {{ item.label }}
          </a>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script setup>
const props = defineProps({
  modelValue: String
})
const items = [
  { key: 'main', label: '主畫面' },
  { key: 'course', label: '選課系統' },
  { key: 'curriculum', label: '課程架構' },
  { key: 'department', label: '系所' },
  { key: 'faculty', label: '師資' }
]
</script>

<style scoped>
/* Modern Navbar Styles */
/* 讓 Navbar 置頂且全寬，現代化美化 */
.navbar {
  width: 100%;
  left: 0;
  top: 0;
  position: sticky;
  z-index: 100;
  background: linear-gradient(90deg, #4f8cff 0%, #38c9fa 100%);
  color: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  font-family: 'Segoe UI', 'Noto Sans TC', Arial, sans-serif;
  margin: 0;
  padding: 0;
}
.navbar-inner {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
}
.brand {
  font-size: 1.7rem;
  font-weight: 700;
  letter-spacing: 2px;
}
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
}
.nav-links a:hover {
  background: rgba(255,255,255,0.15);
  color: #ffe082;
}
.nav-links a.active {
  background: #fff;
  color: #4f8cff;
  font-weight: bold;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-size: 1rem;
}

.nav-links a:hover {
  text-decoration: underline;
}
</style>
