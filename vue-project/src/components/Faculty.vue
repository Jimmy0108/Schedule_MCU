<template>
  <div class="faculty-container">
    <!-- Header -->
    <header class="faculty-header">
      <h1 class="page-title">師資陣容</h1>
      <p class="page-subtitle">年輕有活力的師資團隊，陪你一起成長</p>
      
      <!-- 搜尋框 -->
      <div class="search-box">
        <div class="input-group">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="search-icon">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="搜尋教授姓名或專長..." 
            class="search-input"
            @input="handleSearch" 
          />
          <button v-if="searchQuery" @click="clearSearch" class="clear-btn">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="clear-icon">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </header>

    <!-- Faculty List -->
    <div class="faculty-list-container">
      <div class="filter-tabs">
        <button 
          v-for="filter in filterOptions" 
          :key="filter.value"
          :class="['filter-tab', { active: activeFilter === filter.value }]"
          @click="setFilter(filter.value)"
        >
          {{ filter.label }}
        </button>
      </div>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>正在載入師資資料...</p>
      </div>

      <div v-else-if="error" class="error-state">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="error-icon">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p>無法載入師資資料，請稍後再試</p>
        <button @click="loadTeachers" class="retry-btn">重試</button>
      </div>

      <div v-else-if="filteredTeachers.length === 0" class="empty-state">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="empty-icon">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p v-if="searchQuery">找不到符合「{{ searchQuery }}」的搜尋結果</p>
        <p v-else>目前沒有符合條件的師資資料</p>
      </div>

      <div v-else class="faculty-grid">
        <div class="faculty-card" v-for="teacher in filteredTeachers" :key="teacher.name">
          <div class="card-content">
            <div class="name-title">
              <h3 class="teacher-name">{{ teacher.name }}</h3>
              <div class="title-badge">{{ teacher.title }}</div>
            </div>
            <p v-if="teacher.role" class="teacher-role">{{ teacher.role }}</p>
            <div class="specialization">
              <h4 class="section-title">專長領域</h4>
              <p>{{ teacher.specialization }}</p>
            </div>
            <div class="contact-info">
              <h4 class="section-title">聯絡資訊</h4>
              <div class="contact-item" v-if="teacher.office">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="contact-icon">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                <span>{{ teacher.office }}</span>
              </div>
              <div class="contact-item" v-if="teacher.extension">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="contact-icon">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                </svg>
                <span>分機: {{ teacher.extension }}</span>
              </div>
              <div class="contact-item" v-if="teacher.email">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="contact-icon">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                <a :href="'mailto:' + teacher.email" class="email-link">{{ teacher.email }}</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';

const teachers = ref([]);
const loading = ref(true);
const error = ref(false);
const searchQuery = ref('');
const activeFilter = ref('all');
const BASE_URL = import.meta.env.BASE_URL || '/';

// 過濾選項
const filterOptions = [
  { label: '全部', value: 'all' },
  { label: '教授', value: 'professor' },
  { label: '副教授', value: 'associate' },
  { label: '助理教授', value: 'assistant' },
  { label: '講師', value: 'lecturer' }
];

// 設置過濾器
const setFilter = (filter) => {
  activeFilter.value = filter;
};

// 清除搜尋
const clearSearch = () => {
  searchQuery.value = '';
};

// 處理搜尋輸入
const handleSearch = () => {
  // 搜尋邏輯已由 computed filteredTeachers 處理
};

// 依據搜尋詞與過濾條件篩選教師
const filteredTeachers = computed(() => {
  let result = [...teachers.value];
  
  // 如果有搜尋關鍵詞
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(teacher => 
      teacher.name.toLowerCase().includes(query) || 
      teacher.specialization.toLowerCase().includes(query)
    );
  }
  
  // 依據職位過濾
  if (activeFilter.value !== 'all') {
    if (activeFilter.value === 'professor') {
      result = result.filter(teacher => 
        teacher.title.includes('教授') && 
        !teacher.title.includes('副教授') && 
        !teacher.title.includes('助理教授')
      );
    } else if (activeFilter.value === 'associate') {
      result = result.filter(teacher => 
        teacher.title.includes('副教授')
      );
    } else if (activeFilter.value === 'assistant') {
      result = result.filter(teacher => 
        teacher.title.includes('助理教授')
      );
    } else if (activeFilter.value === 'lecturer') {
      result = result.filter(teacher => 
        teacher.title.includes('講師')
      );
    }
  }
  
  return result;
});

// 載入教師資料
const loadTeachers = async () => {
  loading.value = true;
  error.value = false;
  
  try {
    const response = await fetch(`${BASE_URL}course_data/師資陣容.json`);
    if (!response.ok) {
      throw new Error('網路回應不正確');
    }
    
    const data = await response.json();
    teachers.value = data || [];
    
  } catch (err) {
    console.error('載入師資資料時發生錯誤:', err);
    error.value = true;
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadTeachers();
});
</script>

<style scoped>
@import '../assets/faculty.css';
</style>