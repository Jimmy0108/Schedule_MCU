
<script setup>
import { ref } from 'vue';
import Navbar from './components/Navbar.vue';
import MainScreen from './components/MainScreen.vue';
import CourseSelection from './components/CourseSelection.vue';
import Curriculum from './components/Curriculum.vue';
import Department from './components/Department.vue';
import Faculty from './components/Faculty.vue';

const page = ref('main');
</script>



<template>
  <div id="app">
    <Navbar v-model="page" />
    <main class="content">
      <div v-if="page === 'main'" class="main-center">
        <MainScreen />
      </div>
      <div v-else>
        <CourseSelection v-if="page === 'course'" />
        <Curriculum v-else-if="page === 'curriculum'" />
        <Department v-else-if="page === 'department'" />
        <Faculty v-else-if="page === 'faculty'" />
      </div>
    </main>
  </div>
</template>

<style>
/* Global styles */
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #f4f4f4;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.main-center {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>