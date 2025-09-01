<template>
  <div class="scheduler-container" ref="schedulerRef">
    <div class="schedule-controls">
      <h3 class="schedule-title">我的課表</h3>
      <div class="export-buttons">
        <button class="export-btn" @click="exportSchedule('pdf')" :disabled="exportLoading">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="btn-icon">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          PDF
        </button>
        <button class="export-btn" @click="exportSchedule('png')" :disabled="exportLoading">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="btn-icon">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          PNG
        </button>
        <button class="export-btn" @click="exportSchedule('jpeg')" :disabled="exportLoading">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="btn-icon">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          JPEG
        </button>
      </div>
    </div>

    <div v-if="exportLoading" class="export-overlay">
      <div class="export-loading">
        <svg class="animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" width="24" height="24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span>正在匯出...</span>
      </div>
    </div>

    <div class="schedule-grid" ref="scheduleGridRef">
      <div class="header time-header">時間</div>
      <div v-for="day in days" :key="day" class="header day-header">{{ day }}</div>
      
      <template v-for="slot in timeSlots" :key="slot.label">
        <div class="time-slot">{{ slot.label }}<br><span class="time-range">{{ slot.time }}</span></div>
        <div v-for="day in days" :key="day" class="grid-cell">
          <div 
            v-if="scheduleGrid[day] && scheduleGrid[day][slot.label]" 
            class="course-block"
            :style="getCourseBlockStyle(scheduleGrid[day][slot.label])"
          >
            <p class="course-block-name">{{ scheduleGrid[day][slot.label]['科目'] }}</p>
            <p class="course-block-room">{{ scheduleGrid[day][slot.label]['教室 【地點】'] }}</p>
            <button @click="removeCourse(scheduleGrid[day][slot.label])" class="remove-btn">✕</button>
          </div>
        </div>
      </template>
    </div>

    <div v-if="exportError" class="export-error">{{ exportError }}</div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import useExportSchedule from '../composables/useExportSchedule';

const props = defineProps(['mySchedule']);
const emit = defineEmits(['removeCourse']);

// 匯出功能
const schedulerRef = ref(null);
const scheduleGridRef = ref(null);
const { exportLoading, exportError, exportToPDF, exportToPNG, exportToJPEG } = useExportSchedule();

// 匯出課表
const exportSchedule = async (format) => {
  const element = scheduleGridRef.value;
  if (format === 'pdf') {
    await exportToPDF(element);
  } else if (format === 'png') {
    await exportToPNG(element);
  } else if (format === 'jpeg') {
    await exportToJPEG(element);
  }
};

const days = ['一', '二', '三', '四', '五'];
const timeSlots = [
  { label: '1', time: '08:10-09:00' }, { label: '2', time: '09:10-10:00' },
  { label: '3', time: '10:10-11:00' }, { label: '4', time: '11:10-12:00' },
  { label: '20', time: '12:00-12:50' },
  { label: '5', time: '13:10-14:00' }, { label: '6', time: '14:10-15:00' },
  { label: '7', time: '15:10-16:00' }, { label: '8', time: '16:10-17:00' },
  { label: '9', time: '17:10-18:00' },
  { label: '40', time: '18:00-18:50' },
  { label: '50', time: '18:55-19:45' },
  { label: '60', time: '19:50-20:40' },
  { label: '70', time: '20:45-21:35' },
];

const parseTimeSlots = (timeString) => {
  if (!timeString || typeof timeString !== 'string') return [];
  const dayMap = { '1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '日' };
  const results = [];

  const regex = /星期(\d):([\d\s]+?節)/g;
  let match;
  while ((match = regex.exec(timeString)) !== null) {
    const dayChar = dayMap[match[1]];
    const slotsPart = match[2];
    const slots = slotsPart.match(/\d+/g);
    if (dayChar && slots) {
      slots.forEach(slotStr => {
        const slotNum = parseInt(slotStr, 10);
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

const scheduleGrid = computed(() => {
  const grid = {};
  days.forEach(day => {
    grid[day] = {};
    timeSlots.forEach(slot => {
      grid[day][slot.label] = null;
    });
  });

  props.mySchedule.forEach(course => {
    const parsedTimes = parseTimeSlots(course['上課日期/節次']);
    parsedTimes.forEach(time => {
      if (grid[time.day] && typeof grid[time.day][time.slot] !== 'undefined') {
        grid[time.day][time.slot] = course;
      }
    });
  });
  return grid;
});

// 生成課程顏色 (基於課程類型或系所來區分顏色)
const getCourseBlockStyle = (course) => {
  // 基於課程名稱的雜湊來生成顏色
  const courseType = course['必選修'] || '';
  const department = course['系所名稱'] || course['開課單位'] || '';
  
  // 預設顏色組合
  const colorSets = [
    { bg: 'linear-gradient(135deg, #4361ee, #3a0ca3)', text: 'white' },    // 藍紫
    { bg: 'linear-gradient(135deg, #3a86ff, #0077b6)', text: 'white' },    // 藍色
    { bg: 'linear-gradient(135deg, #2b9348, #007f5f)', text: 'white' },    // 綠色
    { bg: 'linear-gradient(135deg, #ff6b6b, #ef233c)', text: 'white' },    // 紅色
    { bg: 'linear-gradient(135deg, #f77f00, #d62828)', text: 'white' },    // 橙紅
    { bg: 'linear-gradient(135deg, #7209b7, #560bad)', text: 'white' },    // 紫色
    { bg: 'linear-gradient(135deg, #4cc9f0, #4895ef)', text: 'white' },    // 淺藍
  ];
  
  // 基於課程類型選擇顏色
  let colorIndex = 0;
  
  if (courseType.includes('必修')) {
    colorIndex = 0; // 必修課用藍紫色
  } else if (courseType.includes('選修')) {
    colorIndex = 1; // 選修課用藍色
  } else if (department.includes('通識')) {
    colorIndex = 2; // 通識課用綠色
  } else if (department.includes('教育')) {
    colorIndex = 3; // 教育學程用紅色
  } else {
    // 根據課程名稱的第一個字符的ASCII碼來選擇顏色
    const nameChar = (course['科目'] || '').charCodeAt(0) || 0;
    colorIndex = nameChar % colorSets.length;
  }
  
  return { 
    background: colorSets[colorIndex].bg,
    color: colorSets[colorIndex].text
  };
};

const removeCourse = (course) => {
  emit('removeCourse', course);
};
</script>

<style scoped>
.scheduler-container { 
  height: 100%; 
  overflow-y: auto; 
  box-sizing: border-box;
  position: relative;
}

.schedule-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding: 0 0.5rem;
}

.schedule-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.export-buttons {
  display: flex;
  gap: 0.5rem;
}

.export-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  background: linear-gradient(to right, var(--primary), var(--primary-dark));
  color: white;
  border: none;
  border-radius: 6px;
  padding: 0.4rem 0.75rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.export-btn:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  transform: translateY(-1px);
}

.export-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-icon {
  width: 16px;
  height: 16px;
}

.export-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(2px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
  border-radius: 8px;
}

.export-loading {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: white;
  padding: 0.75rem 1.25rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.export-error {
  margin-top: 0.75rem;
  padding: 0.5rem 0.75rem;
  color: #ef4444;
  background-color: #fee2e2;
  border: 1px solid #fecaca;
  border-radius: 6px;
  font-size: 0.875rem;
}

.schedule-grid { 
  display: grid; 
  grid-template-columns: 60px repeat(5, 1fr); 
  grid-auto-rows: minmax(50px, auto); 
  gap: 6px; 
  overflow-x: auto; 
  border-radius: 8px;
  padding: 6px;
  background-color: var(--bg-card);
  box-shadow: var(--shadow-sm);
}

.header { 
  font-weight: 600; 
  font-family: 'Noto Sans TC', sans-serif; 
  text-align: center; 
  padding: 0.5rem; 
  border-radius: 6px; 
  position: sticky; 
  top: 0; 
  z-index: 1; 
  box-shadow: var(--shadow-sm); 
  transition: background 0.3s ease, color 0.3s ease;
}

.day-header {
  background: linear-gradient(to bottom, rgba(67, 97, 238, 0.1), rgba(67, 97, 238, 0.05));
  color: var(--primary);
}

.time-header {
  background: linear-gradient(to bottom, rgba(100, 116, 139, 0.1), rgba(100, 116, 139, 0.05));
  color: var(--text-secondary);
}

.time-slot { 
  font-size: 0.8em; 
  font-weight: 600; 
  text-align: center; 
  padding: 0.5rem; 
  background: rgba(100, 116, 139, 0.05);
  border-radius: 6px; 
  display: flex; 
  flex-direction: column; 
  justify-content: center; 
  align-items: center; 
  box-shadow: var(--shadow-sm); 
  transition: background 0.3s ease, color 0.3s ease;
}

.time-range { 
  font-size: 0.75em; 
  color: var(--text-secondary); 
  font-weight: normal;
}

.grid-cell { 
  border: 1px solid var(--border-color); 
  border-radius: 6px; 
  min-height: 50px; 
  padding: 2px; 
  transition: all 0.15s ease;
  background-color: rgba(255, 255, 255, 0.02);
}
.grid-cell:hover { 
  background-color: rgba(var(--primary-rgb), 0.05); 
}

.break-slot { 
  grid-column: span 1; 
}

.break-cell { 
  grid-column: span 5; 
  background-color: rgba(100, 116, 139, 0.05); 
  display: flex; 
  justify-content: center; 
  align-items: center; 
  font-weight: bold; 
  color: var(--text-secondary); 
}

.course-block { 
  padding: 0.5rem; 
  border-radius: 8px; 
  font-size: 0.8em; 
  position: relative; 
  height: 100%; 
  box-sizing: border-box; 
  box-shadow: var(--shadow-md); 
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.course-block:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
  z-index: 2;
}

.course-block-name { 
  font-weight: 600; 
  margin: 0 0 4px 0; 
  font-family: 'Noto Sans TC', sans-serif;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
  font-size: 0.9em;
  letter-spacing: 0.01em;
}

.course-block-room { 
  margin: 0; 
  font-size: 0.75em;
  opacity: 0.9;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}
.remove-btn { 
  position: absolute; 
  top: 3px; 
  right: 3px; 
  background: rgba(255,255,255,0.15); 
  border: none; 
  color: white; 
  cursor: pointer; 
  font-size: 0.9em; 
  line-height: 1; 
  padding: 3px 5px; 
  opacity: 0.7; 
  border-radius: 4px;
  transition: all 0.15s ease;
}

.remove-btn:hover { 
  opacity: 1; 
  background: rgba(255,255,255,0.25); 
  transform: scale(1.1);
}

/* 深色模式樣式調整 */
:deep(.dark) .schedule-grid {
  background-color: rgba(45, 55, 72, 0.3);
}

:deep(.dark) .grid-cell {
  border-color: rgba(75, 85, 99, 0.3);
  background-color: rgba(0, 0, 0, 0.1);
}

:deep(.dark) .grid-cell:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

:deep(.dark) .day-header {
  background: linear-gradient(to bottom, rgba(123, 137, 244, 0.15), rgba(123, 137, 244, 0.08));
}

:deep(.dark) .time-header,
:deep(.dark) .time-slot {
  background: linear-gradient(to bottom, rgba(45, 55, 72, 0.4), rgba(45, 55, 72, 0.3));
}

/* 響應式設計 */
@media (max-width: 768px) {
  .schedule-controls {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .export-buttons {
    width: 100%;
    justify-content: space-between;
  }
  
  .schedule-grid { 
    grid-template-columns: 50px repeat(5, minmax(160px, 1fr));
    padding-bottom: 8px;
    margin-bottom: 1.5rem;
    -webkit-overflow-scrolling: touch; /* iOS smoother scrolling */
    scrollbar-width: thin; /* Firefox */
  }
  
  .schedule-grid::-webkit-scrollbar {
    height: 6px;
  }
  
  .schedule-grid::-webkit-scrollbar-track {
    background: var(--bg-light);
    border-radius: 10px;
  }
  
  .schedule-grid::-webkit-scrollbar-thumb {
    background: var(--text-secondary);
    opacity: 0.5;
    border-radius: 10px;
  }
  
  .schedule-grid::-webkit-scrollbar-thumb:hover {
    background: var(--text-primary);
    opacity: 0.7;
  }
  
  .schedule-grid::after {
    content: "← 左右滑動查看完整課表 →";
    position: absolute;
    bottom: -1.5rem;
    left: 0;
    right: 0;
    text-align: center;
    font-size: 0.75rem;
    color: var(--text-secondary);
    font-weight: normal;
    pointer-events: none;
  }
}

@media (max-width: 768px) {
  .schedule-grid { 
    grid-template-columns: 50px repeat(5, minmax(160px, 1fr));
    padding-bottom: 8px;
    -webkit-overflow-scrolling: touch; /* iOS smoother scrolling */
    scrollbar-width: thin; /* Firefox */
  }
  
  .schedule-grid::-webkit-scrollbar {
    height: 6px;
  }
  
  .schedule-grid::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
  }
  
  .schedule-grid::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 10px;
  }
  
  .schedule-grid::-webkit-scrollbar-thumb:hover {
    background: #a1a1a1;
  }
  
  .schedule-grid::before {
    content: "← 左右滑動查看課表 →";
    position: absolute;
    bottom: -20px;
    left: 0;
    right: 0;
    text-align: center;
    font-size: 0.75rem;
    color: #888;
    font-weight: normal;
    pointer-events: none;
  }
}
</style>
