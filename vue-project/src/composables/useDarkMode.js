import { ref, watch, onMounted } from 'vue';

export default function useDarkMode() {
    // 檢查本地儲存或系統偏好
    const getThemePreference = () => {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            return savedTheme;
        }
        // 檢查系統偏好
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    };

    const isDark = ref(false);

    // 初始化主題
    const initializeTheme = () => {
        const theme = getThemePreference();
        isDark.value = theme === 'dark';
        applyTheme();
    };

    // 套用主題到 HTML 元素
    const applyTheme = () => {
        if (isDark.value) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
        // 儲存到本地
        localStorage.setItem('theme', isDark.value ? 'dark' : 'light');
    };

    // 切換主題
    const toggleDarkMode = () => {
        isDark.value = !isDark.value;
    };

    // 監聽變化
    watch(isDark, () => {
        applyTheme();
    });

    // 監聽系統主題變化
    const listenForSystemThemeChanges = () => {
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

        // 避免重複儲存的情況下，才根據系統主題來設定
        const handleChange = (e) => {
            if (!localStorage.getItem('theme')) {
                isDark.value = e.matches;
            }
        };

        // 新版和舊版瀏覽器的監聽方式
        if (mediaQuery.addEventListener) {
            mediaQuery.addEventListener('change', handleChange);
        } else if (mediaQuery.addListener) {
            mediaQuery.addListener(handleChange);
        }
    };

    // 在元件掛載時初始化
    onMounted(() => {
        initializeTheme();
        listenForSystemThemeChanges();
    });

    return {
        isDark,
        toggleDarkMode
    };
}
