
<template>
  <div class="main-screen">
    <img src="/src/assets/logo.svg" alt="Logo" class="logo" />
    <h2>歡迎來到銘傳大學選課系統</h2>
    <p class="subtitle">最年輕、最現代的選課體驗</p>
    <p>請使用上方導覽列選擇功能。</p>
  </div>
</template>

<script>
export default {
  name: 'MainScreen'
}
</script>

<style scoped>
.main-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
}
.logo {
  width: 80px;
  margin-bottom: 18px;
  filter: drop-shadow(0 2px 8px rgba(80,120,255,0.12));
}
h2 {
  color: #4f8cff;
  font-size: 2.1rem;
  font-weight: 700;
  margin-bottom: 8px;
}
.subtitle {
  color: #38c9fa;
  font-size: 1.1rem;
  margin-bottom: 18px;
  font-weight: 500;
}
</style>
