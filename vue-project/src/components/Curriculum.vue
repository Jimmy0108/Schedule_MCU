<template>
  <div class="container mx-auto p-4 md:p-8 max-w-7xl">
    <!-- Header -->
    <header class="text-center mb-8">
        <h1 class="text-3xl md:text-4xl font-bold text-blue-800">課程架構</h1>
        <p class="text-lg md:text-xl text-gray-600 mt-2">一目了然的課程規劃，輕鬆掌握學習進度</p>
    </header>

    <!-- Curriculum Table -->
    <div class="bg-white p-6 rounded-xl shadow-md border border-gray-200">
        <div class="overflow-x-auto">
            <table class="min-w-full text-sm text-left text-gray-600">
                <thead class="bg-gray-100 text-xs text-gray-700 uppercase">
                    <tr>
                        <th scope="col" class="px-6 py-3">年級</th>
                        <th scope="col" class="px-6 py-3">必修</th>
                        <th scope="col" class="px-6 py-3">選修</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(row, index) in rows" :key="row.grade" :class="index % 2 === 0 ? 'bg-white' : 'bg-gray-50'" class="border-b">
                        <td class="px-6 py-4 font-medium text-gray-900">{{ row.grade }}</td>
                        <td class="px-6 py-4">{{ row.required }}</td>
                        <td class="px-6 py-4">{{ row.elective }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const rows = ref([
  { grade: '一年級', required: '程式設計、微積分', elective: '英文、體育' },
  { grade: '二年級', required: '電子學、線性代數', elective: '創新思維' },
  { grade: '三年級', required: '資料結構、機率統計', elective: '專題研究' },
  { grade: '四年級', required: '專業實習', elective: '職涯規劃' }
]);
</script>

<style scoped>
/* All styles are now handled by Tailwind CSS, so this block can be empty or removed. */
/* We keep it here for consistency. */
</style>