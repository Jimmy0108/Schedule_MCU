<script setup>
import { ref } from 'vue';
import Navbar from './components/Navbar.vue';
import MainScreen from './components/MainScreen.vue';
import CourseSelection from './components/CourseSelection.vue';
import CourseCurriculum from './components/CourseCurriculum.vue';
import Faculty from './components/Faculty.vue';

const page = ref('main');
</script>

<template>
  <div id="app">
    <!-- Navbar 獨立於內容容器之外 -->
    <Navbar v-model="page" />

    <!-- 主要內容區 -->
    <main class="content">
      <div v-if="page === 'main'" class="main-center">
        <MainScreen @navigate="page = $event" />
      </div>
      <div v-else>
        <CourseSelection v-if="page === 'course'" />
        
        <CourseCurriculum v-else-if="page === 'curriculum_overview'" />
        
        <Faculty v-else-if="page === 'faculty'" />
      </div>
    </main>
  </div>
</template>

<style>
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #f4f4f4;
  display: flex;
  justify-content: center;
  min-height: 100vh;
}

#app {
  width: 100%;
  max-width: 1280px; /* Or any other desired max-width */
  margin: 0 auto;
  font-weight: normal;
}

/* Navbar 樣式 */
.navbar-inner {
  padding: 1rem 2rem;
}

/* 主要內容區 */
.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 2rem;
}

.main-center {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
