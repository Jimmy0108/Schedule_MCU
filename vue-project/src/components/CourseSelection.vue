<template>
  <div class="page-container">
    <!-- 彈出式提示訊息 -->
    <div v-if="conflictMessage" class="conflict-notification">
      <p>{{ conflictMessage }}</p>
      <button @click="conflictMessage = ''">關閉</button>
    </div>

    <!-- 上半部：查詢區 + 課程列表 -->
    <div class="top-section">
      <!-- 左側：課程查詢面板 -->
      <div class="controls-panel">
        <h2>課程查詢</h2>
        
        <div class="control-group">
          <label>課程類型</label>
          <div class="button-group">
            <button 
              v-for="type in courseTypes" 
              :key="type.name"
              :class="{ active: selectedType === type.name }"
              @click="selectCourseType(type)">
              {{ type.displayName }}
            </button>
          </div>
        </div>

        <div class="filters">
          <template v-if="selectedType === '必修課程' || selectedType === '選修課程'">
            <div class="control-group">
              <label for="department-select">系所</label>
              <select id="department-select" v-model="selectedDepartment">
                <option value="all">所有系所</option>
                <option v-for="dept in availableDepartments" :key="dept" :value="dept">
                  {{ dept }}
                </option>
              </select>
            </div>
            <div class="control-group">
              <label for="grade-select">年級</label>
              <select id="grade-select" v-model="selectedGrade">
                <option value="all">所有年級</option>
                <option v-for="grade in availableGrades" :key="grade" :value="grade">
                  {{ grade }} 年級
                </option>
              </select>
            </div>
          </template>

          <template v-else-if="selectedType === '通識課程' || selectedType === '教育學程課程'">
             <div class="control-group">
              <label for="location-select">校區</label>
              <select id="location-select" v-model="selectedLocation">
                <option value="all">所有校區</option>
                <option v-for="loc in availableLocations" :key="loc" :value="loc">
                  {{ loc }}
                </option>
              </select>
            </div>
          </template>
          
          <div class="control-group search-group">
            <label for="course-search">搜尋課程或教師</label>
            <input type="text" id="course-search" v-model="searchQuery" placeholder="例如：微積分 或 王老師">
          </div>
        </div>
      </div>

      <!-- 右側：課程列表 -->
      <div class="course-list-container">
        <div v-if="isLoading" class="loading-state">
          <p>正在載入課程資料...</p>
        </div>
        <div v-else-if="filteredCourses.length > 0">
          <p class="course-count">共找到 {{ filteredCourses.length }} 筆課程</p>
          <ul class="course-list">
            <li v-for="(course, index) in filteredCourses" :key="`${course['科目']}-${index}`" class="course-item">
              <div class="course-info">
                <div class="course-header">
                  <span class="course-name">{{ course['科目'] }}</span>
                  <span class="course-credits">{{ course['學分'] }} 學分</span>
                </div>
                <div class="course-details">
                  <span><strong>教師:</strong> {{ course['任課教師'] }}</span>
                  <span><strong>時間:</strong> {{ course['上課日期/節次'] }}</span>
                  <span><strong>教室:</strong> {{ course['教室 【地點】'] }}</span>
                  <span><strong>選別:</strong> {{ course['選別'] }}</span>
                  <span v-if="course['系所名稱']"><strong>系所:</strong> {{ course['系所名稱'] }} - {{ course['年級'] }} 年級</span>
                  <span v-if="course['查詢校區']"><strong>校區:</strong> {{ course['查詢校區'] }}</span>
                </div>
              </div>
              <button 
                @click="addToSchedule(course)" 
                class="add-button"
                :disabled="isInSchedule(course)"
                :class="{ added: isInSchedule(course) }">
                {{ isInSchedule(course) ? '已加入' : '加入課表' }}
              </button>
            </li>
          </ul>
        </div>
        <div v-else class="empty-state">
          <p>找不到符合條件的課程。</p>
        </div>
      </div>
    </div>

    <!-- 下半部：個人課表 -->
    <div class="scheduler-panel">
      <CourseScheduler 
        :my-schedule="mySchedule"
        @remove-course="removeFromSchedule"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';

import CourseScheduler from './CourseScheduler.vue';

// --- Helper: 解析時間字串 (已修正) ---
const parseTimeSlots = (timeString) => {
  if (!timeString || typeof timeString !== 'string') return [];
  const dayMap = { '1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '日' };
  const results = [];

  // Use regex to find all occurrences of "星期d:..." patterns
  const regex = /星期(\d):([\d\s]+?節)/g;
  let match;
  while ((match = regex.exec(timeString)) !== null) {
    const dayChar = dayMap[match[1]];
    const slotsPart = match[2]; // e.g., "40 50節" or "01 02節"
    const slots = slotsPart.match(/\d+/g);
    if (dayChar && slots) {
      slots.forEach(slotStr => {
        let slotNum;
        if (slotStr.length === 2 && slotStr.endsWith('0')) {
          slotNum = parseInt(slotStr.charAt(0), 10);
        } else {
          slotNum = parseInt(slotStr, 10);
        }
        if (!isNaN(slotNum)) {
          const exists = results.some(r => r.day === dayChar && r.slot === String(slotNum));
          if (!exists) {
            results.push({ day: dayChar, slot: String(slotNum) });
          }
        }
      });
    }
  }
  return results;
};


// --- 資料定義 ---
const courseTypes = [
  { name: '必修課程', displayName: '必修課程', file: 'course_data/必修課程.json' },
  { name: '選修課程', displayName: '選修課程', file: 'course_data/選修課程.json' },
  { name: '通識課程', displayName: '通識課程', file: 'course_data/通識課程.json' },
  { name: '教育學程課程', displayName: '教育學程', file: 'course_data/教育學程課程.json' },
];

// --- 響應式狀態 (State) ---
const isLoading = ref(true);
const selectedType = ref(courseTypes[0].name);
const allCourses = ref([]);
const selectedDepartment = ref('all');
const selectedGrade = ref('all');
const selectedLocation = ref('all');
const searchQuery = ref('');
const mySchedule = ref([]); 
const conflictMessage = ref(''); 

// --- 核心邏輯 (Logic) ---

const loadCourses = async (type) => {
  isLoading.value = true;
  selectedDepartment.value = 'all';
  selectedGrade.value = 'all';
  selectedLocation.value = 'all';
  searchQuery.value = '';
  
  try {
    const response = await fetch(type.file);
    if (!response.ok) throw new Error('Network response was not ok');
    const data = await response.json();
    allCourses.value = data.filter(course => course['科目'] && course['上課日期/節次']);
  } catch (error) {
    console.error('載入課程時發生錯誤:', error);
    allCourses.value = [];
  } finally {
    isLoading.value = false;
  }
};

const selectCourseType = (type) => {
  selectedType.value = type.name;
  loadCourses(type);
};

const addToSchedule = (courseToAdd) => {
  const newCourseTimes = parseTimeSlots(courseToAdd['上課日期/節次']);
  
  if (newCourseTimes.length === 0) {
    conflictMessage.value = `無法加入 "${courseToAdd['科目']}"，因為課程時間格式無法解析。`;
    setTimeout(() => { conflictMessage.value = '' }, 3000);
    return;
  }

  for (const existingCourse of mySchedule.value) {
    const existingCourseTimes = parseTimeSlots(existingCourse['上課日期/節次']);
    for (const newTime of newCourseTimes) {
      for (const existingTime of existingCourseTimes) {
        if (newTime.day === existingTime.day && newTime.slot === existingTime.slot) {
          conflictMessage.value = `課程衝堂！"${courseToAdd['科目']}" 與 "${existingCourse['科目']}" 在星期${newTime.day}第${newTime.slot}節衝突。`;
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
  return mySchedule.value.some(c => c['科目'] === course['科目'] && c['班級'] === course['班級'] && c['任課教師'] === course['任課教師']);
};


// --- 計算屬性 (Computed Properties) ---

const availableDepartments = computed(() => {
  if (!allCourses.value.length) return [];
  const departments = new Set(allCourses.value.map(c => c['系所名稱']).filter(Boolean));
  return Array.from(departments).sort((a, b) => a.localeCompare(b, 'zh-Hant'));
});

const availableGrades = computed(() => {
  if (!allCourses.value.length) return [];
  const grades = new Set(allCourses.value.map(c => c['年級']).filter(g => g !== null && g !== undefined));
  return Array.from(grades).sort((a, b) => {
    const numA = parseInt(a, 10);
    const numB = parseInt(b, 10);
    if (!isNaN(numA) && !isNaN(numB)) {
      return numA - numB;
    }
    return String(a).localeCompare(String(b), 'zh-Hant');
  });
});

const availableLocations = computed(() => {
  if (!allCourses.value.length) return [];
  const locations = new Set(allCourses.value.map(c => c['查詢校區']).filter(Boolean));
  return Array.from(locations).sort((a, b) => a.localeCompare(b, 'zh-Hant'));
});

const filteredCourses = computed(() => {
  let courses = allCourses.value;

  if (selectedType.value === '必修課程' || selectedType.value === '選修課程') {
    if (selectedDepartment.value !== 'all') {
      courses = courses.filter(c => c['系所名稱'] === selectedDepartment.value);
    }
    if (selectedGrade.value !== 'all') {
      courses = courses.filter(c => String(c['年級']) === String(selectedGrade.value));
    }
  } 
  else if (selectedType.value === '通識課程' || selectedType.value === '教育學程課程') {
    if (selectedLocation.value !== 'all') {
      courses = courses.filter(c => c['查詢校區'] === selectedLocation.value);
    }
  }
  
  if (searchQuery.value.trim() !== '') {
    const lowerCaseQuery = searchQuery.value.trim().toLowerCase();
    courses = courses.filter(course => {
      const courseName = String(course['科目'])?.toLowerCase() || '';
      const teacherName = String(course['任課教師'])?.toLowerCase() || '';
      return courseName.includes(lowerCaseQuery) || teacherName.includes(lowerCaseQuery);
    });
  }
  
  return courses;
});

onMounted(() => {
  loadCourses(courseTypes[0]);
});
</script>

<style scoped>
/* 整體佈局 */
.page-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1.5rem;
  background-color: #f0f2f5;
  font-family: 'Segoe UI', sans-serif;
  height: calc(100vh - 60px);
  overflow: hidden;
}

.top-section {
  display: flex;
  gap: 1.5rem;
  flex: 1; 
  min-height: 0;
}

.scheduler-panel {
  flex-shrink: 0; 
  height: 45%; 
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  overflow-y: auto; /* 讓課表可以獨立捲動 */
}

.controls-panel {
  flex: 0 0 380px; 
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  overflow-y: auto;
}

.course-list-container {
  flex: 1; 
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

/* 控制面板樣式 */
.controls-panel h2 { margin-top: 0; color: #333; }
.control-group { margin-bottom: 1.2rem; }
.control-group:last-child { margin-bottom: 0; }
.control-group label { display: block; font-weight: 600; margin-bottom: 0.5rem; color: #555; }
.button-group { display: flex; gap: 0.75rem; flex-wrap: wrap; }
.button-group button { padding: 0.6rem 1.2rem; border: 1px solid #ccc; border-radius: 20px; background: #f9f9f9; cursor: pointer; transition: all 0.2s ease; font-weight: 500; }
.button-group button.active { background: #4f8cff; color: white; border-color: #4f8cff; box-shadow: 0 2px 4px rgba(79, 140, 255, 0.3); }
.button-group button:not(.active):hover { background: #e9ecef; border-color: #adb5bd; }
.filters { display: flex; flex-direction: column; gap: 1.2rem; margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid #eee; }
.filters select, .filters input { padding: 0.6rem; border-radius: 6px; border: 1px solid #ccc; width: 100%; box-sizing: border-box; }

/* 課程列表 */
.course-count { color: #666; font-weight: 500; margin-bottom: 1rem; flex-shrink: 0; }
.course-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 1rem; }
.course-item { display: flex; justify-content: space-between; align-items: center; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem; transition: box-shadow 0.2s ease; }
.course-item:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.course-info { flex-grow: 1; }
.course-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }
.course-name { font-weight: 600; color: #4f8cff; font-size: 1.1rem; }
.course-credits { background-color: #e7f3ff; color: #0056b3; padding: 0.2rem 0.5rem; border-radius: 12px; font-size: 0.8rem; font-weight: 600; }
.course-details { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 0.5rem; font-size: 0.9rem; color: #555; }
.add-button { padding: 0.5rem 1rem; border: none; border-radius: 6px; background-color: #28a745; color: white; cursor: pointer; transition: background-color 0.2s; margin-left: 1rem; white-space: nowrap; }
.add-button:hover:not(:disabled) { background-color: #218838; }
.add-button:disabled { background-color: #aaa; cursor: not-allowed; }
.add-button.added { background-color: #6c757d; }

/* 課表樣式 */
.scheduler-container { height: 100%; overflow-y: auto; box-sizing: border-box; }
.scheduler-container h3 { margin-top: 0; }
.schedule-grid { display: grid; grid-template-columns: 60px repeat(5, 1fr); grid-auto-rows: minmax(50px, auto); gap: 4px; }
.header { font-weight: bold; text-align: center; padding: 0.5rem; background-color: #f8f9fa; border-radius: 4px; position: sticky; top: 0; z-index: 1; }
.time-slot { font-size: 0.8em; font-weight: bold; text-align: center; padding: 0.5rem; background-color: #f8f9fa; border-radius: 4px; display: flex; flex-direction: column; justify-content: center; align-items: center; }
.time-range { font-size: 0.8em; color: #6c757d; }
.grid-cell { border: 1px solid #eee; border-radius: 4px; min-height: 50px; padding: 2px; }
.break-slot { grid-column: span 1; }
.break-cell { grid-column: span 5; background-color: #f8f9fa; display: flex; justify-content: center; align-items: center; font-weight: bold; color: #6c757d; }
.course-block { background-color: #4f8cff; color: white; padding: 0.5rem; border-radius: 4px; font-size: 0.8em; position: relative; height: 100%; box-sizing: border-box; }
.course-block-name { font-weight: bold; margin: 0 0 4px 0; }
.course-block-room { margin: 0; }
.remove-btn { position: absolute; top: 2px; right: 2px; background: none; border: none; color: white; cursor: pointer; font-size: 1.2em; line-height: 1; padding: 0; opacity: 0.6; }
.remove-btn:hover { opacity: 1; }

/* 提示訊息樣式 */
.conflict-notification { position: fixed; top: 80px; left: 50%; transform: translateX(-50%); background-color: #dc3545; color: white; padding: 1rem 1.5rem; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); z-index: 1000; display: flex; align-items: center; gap: 1rem; }
.conflict-notification button { background: white; color: #dc3545; border: none; padding: 0.3rem 0.8rem; border-radius: 4px; cursor: pointer; }

/* 狀態提示 */
.loading-state, .empty-state { text-align: center; padding: 3rem; color: #888; }
</style>
