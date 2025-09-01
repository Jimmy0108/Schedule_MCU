<template>
  <div class="container mx-auto p-4 md:p-8 max-w-7xl">
    <header class="mb-4 md:mb-8">
      <div class="flex items-center justify-between">
        <div>
          <h1
            class="text-2xl md:text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-800 via-indigo-700 to-purple-800 font-noto">
            選課系統
          </h1>
          <p class="text-sm md:text-xl text-gray-600 mt-1 md:mt-2 font-inter">輕鬆查詢課程，打造專屬課表</p>
        </div>
        <button
          class="md:hidden inline-flex items-center px-4 py-2 rounded-lg bg-gradient-to-r from-blue-700 to-indigo-700 text-white shadow-md"
          @click="showFilters = true">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
          </svg>
          篩選
        </button>
      </div>
    </header>

    <!-- 課程區塊 -->
    <div class="bg-white p-6 rounded-xl shadow-lg mb-8 border border-gray-100 transition-shadow hover:shadow-xl">
      <div v-if="conflictMessage" class="conflict-notification">
        <svg class="w-5 h-5 mr-2 text-white" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"
          fill="currentColor">
          <path fill-rule="evenodd"
            d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
            clip-rule="evenodd" />
        </svg>
        <p>{{ conflictMessage }}</p>
        <button @click="conflictMessage = ''" class="hover:bg-red-600 transition p-1 rounded-full ml-2">
          <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd"
              d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
              clip-rule="evenodd" />
          </svg>
        </button>
      </div>

      <div class="top-section">
        <!-- 篩選控制區 -->
        <div class="controls-panel" :class="{ 'mobile-drawer': isMobile, 'drawer-open': isMobile && showFilters }">
          <div class="drawer-header md:hidden" v-if="isMobile">
            <h3 class="text-lg font-semibold font-noto">篩選條件</h3>
            <button class="text-gray-500 hover:text-gray-700 p-2 rounded-full transition" @click="showFilters = false">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clip-rule="evenodd" />
              </svg>
            </button>
          </div>
          <h2>課程查詢</h2>

          <div class="control-group">
            <label>課程類型</label>
            <div class="button-group">
              <button v-for="type in courseTypes" :key="type.name" :class="{ active: selectedType === type.name }"
                @click="selectCourseType(type.name)">
                {{ type.displayName }}
              </button>
            </div>
          </div>

          <div class="filters">
            <template v-if="selectedType === '必修' || selectedType === '選修'">
              <div class="control-group">
                <label for="department-select">系所</label>
                <select id="department-select" v-model="selectedDepartment">
                  <option value="all">所有系所</option>
                  <option v-for="dept in availableDepartments" :key="dept" :value="dept">{{ dept }}</option>
                </select>
              </div>
              <div class="control-group">
                <label for="grade-select">年級</label>
                <select id="grade-select" v-model="selectedGrade">
                  <option value="all">所有年級</option>
                  <option v-for="grade in availableGrades" :key="grade" :value="grade">{{ grade }}</option>
                </select>
              </div>
            </template>

            <template v-else-if="selectedType === '通識' || selectedType === '教育'">
              <div class="control-group">
                <label for="location-select">校區</label>
                <select id="location-select" v-model="selectedLocation">
                  <option value="all">所有校區</option>
                  <option v-for="loc in availableLocations" :key="loc" :value="loc">{{ loc }}</option>
                </select>
              </div>
            </template>

            <div class="control-group search-group">
              <label for="course-search">搜尋課程或教師</label>
              <input type="text" id="course-search" v-model="searchQuery" placeholder="例如：微積分 或 王老師">
            </div>
          </div>
        </div>

        <!-- 課程清單 -->
        <div class="course-list-container">
          <div class="md:hidden mb-4 flex flex-wrap items-center gap-2" v-if="activeFilterChips.length">
            <span v-for="chip in activeFilterChips" :key="chip"
              class="px-3 py-1 text-xs rounded-full bg-gradient-to-r from-blue-50 to-indigo-50 text-indigo-700 border border-blue-100 shadow-sm flex items-center">
              {{ chip }}
            </span>
            <button
              class="ml-auto text-sm text-indigo-600 px-3 py-1 rounded-lg border border-indigo-100 bg-indigo-50 flex items-center"
              @click="clearAllFilters">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clip-rule="evenodd" />
              </svg>
              清除
            </button>
          </div>
          <div v-if="isLoading" class="loading-state">
            <p>正在載入課程資料...</p>
          </div>
          <div v-else-if="filteredCourses.length > 0">
            <p class="course-count">共找到 {{ filteredCourses.length }} 筆課程</p>
            <ul class="course-list">
              <li v-for="(course, index) in paginatedCourses"
                :key="`${course['科目代碼']}-${course['班級代號']}-${index}`" class="course-item">
                <div class="course-info">
                  <div class="course-header">
                    <span class="course-name">{{ course['科目名稱'] }}</span>
                    <span class="course-credits">{{ course['學分'] }} 學分</span>
                  </div>
                  <div class="course-details">
                    <span><strong>科目代碼:</strong> {{ course['科目代碼'] }}</span>
                    <span><strong>班級:</strong> {{ course['班級名稱'] ? `${course['班級名稱']} (${course['班級代號']})` : course['班級代號'] }}</span>
                    <span><strong>教師:</strong> {{ course['任課教師'] }}</span>
                    <span><strong>時間:</strong> {{ course['上課日期/節次'] }}</span>
                    <span><strong>教室:</strong> {{ course['教室 【地點】'] }}</span>
                    <span><strong>選別:</strong> {{ course['選別'] }}</span>
                    <span v-if="course['完整系所']"><strong>系所:</strong> {{ course['完整系所'] }}</span>
                    <span v-if="course['查詢校區']"><strong>校區:</strong> {{ course['查詢校區'] }}</span>
                  </div>
                </div>
                <button @click="addToSchedule(course)" class="add-button" :disabled="isInSchedule(course)"
                  :class="{ added: isInSchedule(course) }">
                  {{ isInSchedule(course) ? '已加入' : '加入課表' }}
                </button>
              </li>
            </ul>
            <!-- Pagination Controls -->
            <div v-if="totalPages > 1" class="pagination-controls">
              <button @click="prevPage" :disabled="currentPage === 1" class="pagination-button">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
                <span>上一頁</span>
              </button>
              <span class="pagination-info">第 {{ currentPage }} / {{ totalPages }} 頁</span>
              <button @click="nextPage" :disabled="currentPage === totalPages" class="pagination-button">
                <span>下一頁</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
          <div v-else class="empty-state">
            <p>找不到符合條件的課程。</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 我的課表 -->
    <div id="my-schedule"
      class="bg-white p-6 rounded-xl shadow-lg border border-gray-100 transition-shadow hover:shadow-xl relative">
      <div
        class="absolute -top-3 left-5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-4 py-1 rounded-full text-sm font-medium shadow-md">
        我的課表
      </div>
      <div class="mt-3">
        <CourseScheduler :my-schedule="mySchedule" @remove-course="removeFromSchedule" />
      </div>
    </div>

    <button class="md:hidden fixed bottom-6 right-6 rounded-full bg-blue-600 text-white shadow-lg px-4 py-3"
      @click="scrollToSchedule" aria-label="前往我的課表">
      查看課表
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, onBeforeUnmount } from 'vue';
import CourseScheduler from './CourseScheduler.vue';

/** ========= Helper: 解析上課時間 ========= */
const parseTimeSlots = (timeString) => {
  if (!timeString || typeof timeString !== 'string') return [];
  const dayMap = { '1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '0': '日' };
  const results = [];
  const regex = /星期(\d):([\d\s]+?節)/g;
  let match;
  while ((match = regex.exec(timeString)) !== null) {
    const dayChar = dayMap[match[1]];
    const slotsPart = match[2];
    const slots = slotsPart.match(/\d+/g);
    if (dayChar && slots) {
      slots.forEach(slotStr => {
        const normalized = String(parseInt(slotStr, 10)).padStart(2, '0');
        if (['40', '50', '60', '70'].includes(slotStr)) {
          const exists = results.some(r => r.day === dayChar && r.slot === slotStr);
          if (!exists) results.push({ day: dayChar, slot: slotStr });
        } else if (normalized && !isNaN(Number(normalized))) {
          const exists = results.some(r => r.day === dayChar && r.slot === normalized);
          if (!exists) results.push({ day: dayChar, slot: normalized });
        }
      });
    }
  }
  return results;
};

/** ========= Helper: 提取校區 ========= */
const extractLocation = (roomStr) => {
  if (!roomStr || typeof roomStr !== 'string') return '';
  const match = roomStr.match(/【(.+?)】/);
  return (match && match[1]) ? match[1] : '';
};

/** ========= 靜態定義 ========= */
const courseTypes = [
  { name: 'all', displayName: '全部課程' },
  { name: '必修', displayName: '必修課程' },
  { name: '選修', displayName: '選修課程' },
  { name: '通識', displayName: '通識課程' },
  { name: '教育', displayName: '教育學程' },
];

/** ========= 響應式狀態 ========= */
const isLoading = ref(true);
const selectedType = ref('all');
const allCourses = ref([]);
const selectedDepartment = ref('all');
const selectedGrade = ref('all');
const selectedLocation = ref('all');
const searchQuery = ref('');
const mySchedule = ref([]);
const conflictMessage = ref('');
const currentPage = ref(1);
const itemsPerPage = ref(5);
const isMobile = ref(false);
const showFilters = ref(false);

/** ========= 核心邏輯：讀取 JSON + 處理 ========= */
const loadAllCourses = async () => {
  isLoading.value = true;
  try {
    // 從多個 JSON 檔案讀取課程資料
    let requiredCourses = [], electiveCourses = [], educationCourses = [], generalCourses = [];
    
    try {
      requiredCourses = await fetch(`${import.meta.env.BASE_URL}course_data/必修課程.json`).then(res => res.json());
      console.log('成功載入必修課程');
    } catch (e) {
      console.error('無法載入必修課程:', e);
    }
    
    try {
      electiveCourses = await fetch(`${import.meta.env.BASE_URL}course_data/選修課程.json`).then(res => res.json());
      console.log('成功載入選修課程');
    } catch (e) {
      console.error('無法載入選修課程:', e);
    }
    
    try {
      educationCourses = await fetch(`${import.meta.env.BASE_URL}course_data/教育學程課程.json`).then(res => res.json());
      console.log('成功載入教育學程課程');
    } catch (e) {
      console.error('無法載入教育學程課程:', e);
    }
    
    try {
      generalCourses = await fetch(`${import.meta.env.BASE_URL}course_data/通識課程.json`).then(res => res.json());
      console.log('成功載入通識課程');
    } catch (e) {
      console.log('無法載入通識課程（可選）:', e);
    }

    const combined = [...requiredCourses, ...electiveCourses, ...educationCourses, ...generalCourses];

    allCourses.value = combined.map(course => {
      const parsedCourse = { ...course };

      // === 科目代碼/名稱 ===
      if (typeof course['科目'] === 'string') {
        const parts = course['科目'].split(' ');
        parsedCourse['科目代碼'] = parts[0] || '';
        parsedCourse['科目名稱'] = parts.slice(1).join(' ') || '';
      } else {
        parsedCourse['科目代碼'] = '';
        parsedCourse['科目名稱'] = course['科目'] || '';
      }

      // === 班級解析 ===
      const classStr = String(course['班級'] || '').trim();
      let classCode = '';
      let deptFromClass = '';
      let gradeFromClass = '';
      let className = '';

      if (/^\d+$/.test(classStr)) {
        // 純數字形式的班級代號
        classCode = classStr;
      } else {
        // 代碼+系所年級班別 形式的班級
        const match = classStr.match(/^(\d+)\s*(.+)$/);
        if (match) {
          classCode = match[1];
          const rest = match[2];
          // 嘗試解析系所、年級和班別
          const gradeMatch = rest.match(/(.+?)([一二三四\d]+)([甲乙丙丁]?)$/);
          if (gradeMatch) {
            deptFromClass = gradeMatch[1];
            const gradeRaw = gradeMatch[2];
            className = gradeMatch[3] || '';
            
            // 中文數字轉換
            const chineseToNum = { '一': '1', '二': '2', '三': '3', '四': '4' };
            if (chineseToNum[gradeRaw]) gradeFromClass = `${chineseToNum[gradeRaw]} 年級`;
            else if (!isNaN(Number(gradeRaw))) gradeFromClass = `${gradeRaw} 年級`;
            else gradeFromClass = gradeRaw;
          } else {
            deptFromClass = rest;
          }
        }
      }
      parsedCourse['班級代號'] = classCode;
      parsedCourse['班級名稱'] = className;

      // === 年級處理 ===
      let displayGrade = '';
      const grade = String(course['年級'] || '').trim();
      if (grade === '0') displayGrade = '不分年級';
      else if (!isNaN(parseInt(grade, 10)) && parseInt(grade, 10) > 0) displayGrade = `${grade} 年級`;
      else displayGrade = grade || '';
      
      // 優先使用原始年級數據，若無則使用從班級解析出的年級
      parsedCourse['年級'] = displayGrade || gradeFromClass;

      // === 系所 ===
      parsedCourse['系所名稱'] = course['系所名稱'] || deptFromClass || '';
      
      // 完整系所：將「系所名稱 + 年級」合併，用於顯示與篩選
      if (parsedCourse['系所名稱'] && parsedCourse['年級']) {
        parsedCourse['完整系所'] = `${parsedCourse['系所名稱']} - ${parsedCourse['年級']}`;
      } else if (parsedCourse['系所名稱']) {
        parsedCourse['完整系所'] = parsedCourse['系所名稱'];
      } else if (parsedCourse['年級']) {
        parsedCourse['完整系所'] = parsedCourse['年級'];
      } else {
        parsedCourse['完整系所'] = '';
      }

      // === 校區 ===
      parsedCourse['查詢校區'] = extractLocation(course['教室 【地點】']);

      // === 上課時間 ===
      parsedCourse.parsedTime = parseTimeSlots(course['上課日期/節次']);

      return parsedCourse;
    }).filter(c => c['科目名稱']); // 過濾掉沒有名稱的課程
  } catch (error) {
    console.error("處理課程資料時發生錯誤:", error);
    allCourses.value = [];
  } finally {
    isLoading.value = false;
  }
};

/** ========= 事件處理與使用者互動 ========= */
const selectCourseType = (typeName) => {
  selectedType.value = typeName;
  clearAllFilters(false); // 清除篩選，但不重置課程類型
  currentPage.value = 1; // 重置分頁
};

const addToSchedule = (courseToAdd) => {
  if (isInSchedule(courseToAdd)) {
    conflictMessage.value = `"${courseToAdd['科目名稱']}" 已經在您的課表中了。`;
    setTimeout(() => { conflictMessage.value = '' }, 3000);
    return;
  }
  
  const newCourseTimes = courseToAdd.parsedTime;
  if (newCourseTimes.length === 0) {
    conflictMessage.value = `無法加入 "${courseToAdd['科目名稱']}"，因為課程時間格式無法解析。`;
    setTimeout(() => { conflictMessage.value = '' }, 3000);
    return;
  }

  // 檢查衝堂
  for (const existingCourse of mySchedule.value) {
    for (const newTime of newCourseTimes) {
      for (const existingTime of existingCourse.parsedTime) {
        if (newTime.day === existingTime.day && newTime.slot === existingTime.slot) {
          conflictMessage.value = `課程衝堂！"${courseToAdd['科目名稱']}" 與 "${existingCourse['科目名稱']}" 在星期${newTime.day}第${newTime.slot}節衝突。`;
          setTimeout(() => { conflictMessage.value = '' }, 3000);
          return;
        }
      }
    }
  }
  
  mySchedule.value.push(courseToAdd);
};

const removeFromSchedule = (courseToRemove) => {
  mySchedule.value = mySchedule.value.filter(c => c !== courseToRemove);
};

const isInSchedule = (course) => {
  return mySchedule.value.some(c => 
    c['科目代碼'] === course['科目代碼'] && 
    c['班級代號'] === course['班級代號']
  );
};

const clearAllFilters = (resetType = true) => {
  if(resetType) selectedType.value = 'all';
  selectedDepartment.value = 'all';
  selectedGrade.value = 'all';
  selectedLocation.value = 'all';
  searchQuery.value = '';
  currentPage.value = 1;
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

const scrollToSchedule = () => {
  const el = document.getElementById('my-schedule');
  if (el) el.scrollIntoView({ behavior: 'smooth' });
  showFilters.value = false; // 關閉篩選選單
};

/** ========= 計算屬性 ========= */
// 根據選擇的類型過濾課程
const currentCourseSet = computed(() => {
  if (selectedType.value === 'all') {
    return allCourses.value;
  }
  return allCourses.value.filter(c => c['選別'] === selectedType.value);
});

// 可用系所列表
const availableDepartments = computed(() => {
  const departments = new Set(
    currentCourseSet.value
      .map(c => c['系所名稱'])
      .filter(Boolean)
  );
  return Array.from(departments).sort((a, b) => a.localeCompare(b, 'zh-Hant'));
});

// 可用年級列表
const availableGrades = computed(() => {
  const grades = new Set(
    currentCourseSet.value
      .map(c => c['年級'])
      .filter(Boolean)
  );
  return Array.from(grades).sort((a, b) => {
    const numA = parseInt(a, 10);
    const numB = parseInt(b, 10);
    if (!isNaN(numA) && !isNaN(numB)) return numA - numB;
    return String(a).localeCompare(String(b), 'zh-Hant');
  });
});

// 可用校區列表
const availableLocations = computed(() => {
  const locations = new Set(
    currentCourseSet.value
      .map(c => c['查詢校區'])
      .filter(Boolean)
  );
  return Array.from(locations).sort((a, b) => a.localeCompare(b, 'zh-Hant'));
});

// 篩選後的課程
const filteredCourses = computed(() => {
  let courses = currentCourseSet.value;

  // 系所篩選
  if (selectedDepartment.value !== 'all') {
    courses = courses.filter(c => c['系所名稱'] === selectedDepartment.value);
  }

  // 年級篩選
  if (selectedGrade.value !== 'all') {
    courses = courses.filter(c => c['年級'] === selectedGrade.value);
  }

  // 校區篩選
  if (selectedLocation.value !== 'all') {
    courses = courses.filter(c => c['查詢校區'] === selectedLocation.value);
  }
  
  // 關鍵字搜尋 (課程名稱或教師)
  if (searchQuery.value.trim() !== '') {
    const query = searchQuery.value.trim().toLowerCase();
    courses = courses.filter(course => {
      const courseName = String(course['科目名稱'] || '').toLowerCase();
      const teacherName = String(course['任課教師'] || '').toLowerCase();
      return courseName.includes(query) || teacherName.includes(query);
    });
  }
  
  return courses;
});

// 總頁數
const totalPages = computed(() => {
  return Math.ceil(filteredCourses.value.length / itemsPerPage.value) || 1;
});

// 當前頁面的課程
const paginatedCourses = computed(() => {
  // 統一使用分頁邏輯
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return filteredCourses.value.slice(start, end);
});

// 顯示中的篩選條件
const activeFilterChips = computed(() => {
  const chips = [];
  
  // 課程類型
  if (selectedType.value !== 'all') {
    const typeDisplay = courseTypes.find(t => t.name === selectedType.value)?.displayName;
    if (typeDisplay) chips.push(typeDisplay);
  }
  
  // 系所、年級、校區
  if (selectedDepartment.value !== 'all') chips.push(`系所: ${selectedDepartment.value}`);
  if (selectedGrade.value !== 'all') chips.push(`年級: ${selectedGrade.value}`);
  if (selectedLocation.value !== 'all') chips.push(`校區: ${selectedLocation.value}`);
  
  // 搜尋關鍵字
  if (searchQuery.value.trim()) chips.push(`關鍵字: ${searchQuery.value.trim()}`);
  
  return chips;
});

// 監聽篩選條件變更，重置分頁
watch([selectedType, selectedDepartment, selectedGrade, selectedLocation, searchQuery], () => {
  currentPage.value = 1;
});

/** ========= 生命週期 ========= */
// 響應式調整行動/桌面版
const handleResize = () => {
  const windowWidth = window.innerWidth;
  isMobile.value = windowWidth < 768;
  
  // 在桌面模式時自動關閉行動版篩選器
  if (!isMobile.value) showFilters.value = false;
};

onMounted(() => {
  // 載入課程
  loadAllCourses();
  
  // 初始化並監聽視窗大小變更
  handleResize();
  window.addEventListener('resize', handleResize);
});

onBeforeUnmount(() => { 
  window.removeEventListener('resize', handleResize);
});
</script>

<style scoped>
/* 整體容器與佈局 */
.container {
  font-family: 'Inter', 'Noto Sans TC', sans-serif;
  min-height: 100vh;
}

.top-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

@media (min-width: 768px) {
  .top-section {
    flex-direction: row;
  }
}

/* 彈出式訊息 */
.conflict-notification {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #ef4444;
  color: white;
  padding: 0.75rem 1.25rem;
  border-radius: 0.5rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  z-index: 1100;
  display: flex;
  align-items: center;
  max-width: 90%;
}

/* 控制面板 - 篩選區域 */
.controls-panel {
  flex: 0 0 280px;
  padding: 1.5rem;
  background: #fff;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.controls-panel h2 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 1.25rem;
  font-family: 'Noto Sans TC', sans-serif;
  color: #1f2937;
}

.control-group {
  margin-bottom: 1.25rem;
}

.control-group label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #4b5563;
  margin-bottom: 0.5rem;
  display: block;
}

.button-group {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.button-group button {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 9999px;
  background-color: #f9fafb;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.875rem;
}

.button-group button.active {
  background: linear-gradient(to right, #4f46e5, #7c3aed);
  color: white;
  border-color: transparent;
}

.button-group button:hover:not(.active) {
  background-color: #f3f4f6;
}

.filters {
  border-top: 1px solid #e5e7eb;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
}

.filters select,
.filters input {
  width: 100%;
  padding: 0.6rem 0.75rem;
  border-radius: 0.375rem;
  border: 1px solid #d1d5db;
  background-color: #f9fafb;
  transition: all 0.2s;
}

.filters select:focus,
.filters input:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
}

/* 課程列表 */
.course-list-container {
  flex: 1;
  min-width: 0;
}

.course-count {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 1rem;
}

.course-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.course-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  padding: 1rem;
  transition: all 0.2s ease;
  background-color: #fff;
}

.course-item:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transform: translateY(-2px);
}

.course-info {
  flex-grow: 1;
  margin-right: 1rem;
}

.course-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.course-name {
  font-weight: 700;
  color: #374151;
  font-size: 1.125rem;
  font-family: 'Noto Sans TC', sans-serif;
}

.course-credits {
  background-color: #eef2ff;
  color: #4338ca;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

.course-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #4b5563;
}

.course-details strong {
  color: #374151;
}

.add-button {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  background-color: #4f46e5;
  color: white;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
  font-weight: 600;
  align-self: center;
}

.add-button:hover:not(:disabled) {
  background-color: #4338ca;
}

.add-button:disabled,
.add-button.added {
  background-color: #a5b4fc;
  cursor: not-allowed;
}

.loading-state,
.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  color: #6b7280;
  font-style: italic;
  background-color: #f9fafb;
  border-radius: 0.5rem;
  border: 1px dashed #e5e7eb;
}

/* 分頁控制 */
.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 2rem;
  padding: 0.5rem;
  user-select: none;
}

.pagination-button {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  background-color: #fff;
  font-weight: 600;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pagination-button:hover:not(:disabled) {
  background-color: #f3f4f6;
  border-color: #a5b4fc;
}

.pagination-button:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
}

.pagination-button:disabled {
  background-color: #f9fafb;
  color: #9ca3af;
  cursor: not-allowed;
  border-color: #e5e7eb;
}

.pagination-info {
  margin: 0 1rem;
  font-size: 0.875rem;
  color: #4b5563;
  font-weight: 500;
  min-width: 80px;
  text-align: center;
}


/* 行動裝置樣式 - 修復側邊欄溢出問題 */
@media (max-width: 767px) {
  .container {
    padding: 1rem;
    overflow-x: hidden; /* 防止側邊欄溢出 */
  }
  
  /* 隱藏默認控制面板 */
  .controls-panel {
    display: none;
  }
  
  /* 行動版抽屜式篩選面板 */
  .mobile-drawer {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 1000;
    display: none;
    overflow: hidden;
  }
  
  .mobile-drawer.drawer-open {
    display: block;
  }
  
  .mobile-drawer .drawer-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 1rem;
    border-bottom: 1px solid #e5e7eb;
    margin-bottom: 1rem;
  }
  
  .mobile-drawer::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: -1;
  }
  
  .mobile-drawer > div {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    max-height: 85vh;
    background: white;
    border-top-left-radius: 1rem;
    border-top-right-radius: 1rem;
    padding: 1.5rem;
    overflow-y: auto;
    box-shadow: 0 -4px 10px rgba(0, 0, 0, 0.1);
    z-index: 1001;
    box-sizing: border-box;
  }
  
  .course-item {
    flex-direction: column;
  }
  
  .add-button {
    width: 100%;
    margin-top: 0.75rem;
  }
  
  .course-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .course-details {
    grid-template-columns: 1fr;
  }
}
</style>
