<template>
  <div class="container mx-auto p-4 md:p-8 max-w-7xl">
    <!-- Header -->
    <header class="text-center mb-8">
        <h1 class="text-3xl md:text-4xl font-bold text-blue-800">師資陣容</h1>
        <p class="text-lg md:text-xl text-gray-600 mt-2">年輕有活力的師資團隊，陪你一起成長</p>
    </header>

    <!-- Faculty List -->
    <div class="bg-white p-6 rounded-xl shadow-md border border-gray-200">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div class="faculty-card p-5 rounded-lg shadow border border-gray-100 flex flex-col justify-between" v-for="teacher in teachers" :key="teacher.name">
                <div>
                    <h3 class="font-bold text-gray-800 text-lg mb-2">{{ teacher.name }}</h3>
                    <p class="text-sm text-gray-500 mb-1">{{ teacher.title }}</p>
                    <p v-if="teacher.role" class="text-xs text-gray-400 mb-2">{{ teacher.role }}</p>
                    <p class="text-sm text-gray-600 leading-relaxed">專長：{{ teacher.specialization }}</p>
                </div>
                <div class="mt-4 text-xs text-gray-500">
                    <p v-if="teacher.office">辦公室: {{ teacher.office }}</p>
                    <p v-if="teacher.extension">分機: {{ teacher.extension }}</p>
                    <p v-if="teacher.email">Email: <a :href="'mailto:' + teacher.email" class="text-blue-500 hover:underline">{{ teacher.email }}</a></p>
                </div>
            </div>
        </div>
        <div v-if="teachers.length === 0" class="text-center text-gray-500 py-8">
            <p>載入師資資料中...</p>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const teachers = ref([]);

onMounted(async () => {
  try {
    // Using web_fetch to get the content
    const response = await fetch('https://ele.mcu.edu.tw/%E5%B0%88%E4%BB%BB%E6%95%99%E5%B8%AB/');
    const text = await response.text();

    // Regex to parse the data
    const regex = /Name:\s*(.*?)\s*Title:\s*(.*?)\s*Role:\s*(.*?)\s*Specialization:\s*(.*?)\s*Office Location:\s*(.*?)\s*Extension:\s*(.*?)\s*Email:\s*(.*?)(?=\n\nName:|$)/gs;
    let match;
    const parsedTeachers = [];

    while ((match = regex.exec(text)) !== null) {
      parsedTeachers.push({
        name: match[1].trim(),
        title: match[2].trim(),
        role: match[3].trim(),
        specialization: match[4].trim(),
        office: match[5].trim(),
        extension: match[6].trim(),
        email: match[7].trim()
      });
    }
    teachers.value = parsedTeachers;

  } catch (error) {
    console.error('Error fetching or parsing faculty data:', error);
    teachers.value = []; // Clear teachers on error
  }
});
</script>

<style scoped>
/* Tailwind CSS handles most styling, but keep this for specific overrides if needed */
</style>