<template>
  <div class="scheduler-container">
    <h3>我的課表</h3>
    <div class="schedule-grid">
      <div class="header">時間</div>
      <div v-for="day in days" :key="day" class="header">{{ day }}</div>
      
      <template v-for="slot in timeSlots" :key="slot.label">
        <div class="time-slot">{{ slot.label }}<br><span class="time-range">{{ slot.time }}</span></div>
        <div v-for="day in days" :key="day" class="grid-cell">
          <div v-if="scheduleGrid[day] && scheduleGrid[day][slot.label]" class="course-block">
            <p class="course-block-name">{{ scheduleGrid[day][slot.label]['科目'] }}</p>
            <p class="course-block-room">{{ scheduleGrid[day][slot.label]['教室 【地點】'] }}</p>
            <button @click="removeCourse(scheduleGrid[day][slot.label])" class="remove-btn">✕</button>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps(['mySchedule']);
const emit = defineEmits(['removeCourse']);

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

const removeCourse = (course) => {
  emit('removeCourse', course);
};
</script>

<style scoped>
.scheduler-container { height: 100%; overflow-y: auto; box-sizing: border-box; }
.scheduler-container h3 { margin-top: 0; color: #333; }
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
</style>
