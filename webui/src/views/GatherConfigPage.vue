<template>
    <div class="m-2">
        <!-- 设置坐标 -->
        <div class="flex mt-4 w-full  align-items-center">
            <label class="w-6">最晚通知时间(单位:秒)</label>
            <input type="text" v-model="config.notification_delay"
                class="w-6 text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary"
                placeholder="检测周期(s)">
        </div>
        <div class="flex mt-4 w-full  align-items-center">
            <label class="w-6">通知时间频率(单位:秒)</label>
            <input type="text" v-model="config.notification_interval"
                class="w-6 text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary"
                placeholder="检测周期(s)">
        </div>
        <div class="flex mt-4 w-full  align-items-center">
            <label class="w-6">检测频率(单位:秒)</label>
            <input type="text" v-model="config.gather_detection_interval"
                class="w-6 text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary"
                placeholder="检测周期(s)">
        </div>

        <div class="w-full mt-4">
            <Button class="w-full justify-content-center" size="small" @click="saveConfig">
                <div>保存配置</div>
            </Button>
        </div>
        <Button class="w-full justify-content-center mt-4" size="small"
            @click="router.push({ path: '/' })">返回主菜单</Button>
        <Toast />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import 'vue-advanced-cropper/dist/style.css';
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';

const config = ref({
    notification_delay: 180,
    notification_interval: 15,
    gather_detection_interval: 60,
})
const cropperView = ref(null);
const img = "http://localhost:8000/images/target.jpg";
const imgLoading = ref(false);
function change({ coordinates, canvas }) {
    config.value.detect_region_x = coordinates.left
    config.value.detect_region_y = coordinates.top
    config.value.detect_region_w = coordinates.width
    config.value.detect_region_h = coordinates.height
    console.log(coordinates)
}
const toast = useToast();
const router = useRouter();


onMounted(() => {
})

</script>