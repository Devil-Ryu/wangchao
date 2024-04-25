<template>
    <div class="m-2">
        <!-- 设置坐标 -->
        <div class="flex mt-2 w-full  align-items-center">
            <div class="flex w-6 justify-content-between align-items-center">
                <label class="w-6">地图坐标X</label>
                <input type="text" v-model="config.target_area_x"
                    class="w-6 ml-2 mr-2 text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary"
                    placeholder="坐标X">
            </div>
            <div class="flex w-6 justify-content-between align-items-center">
                <label class="w-6 ml-2">地图坐标Y</label>
                <input type="text" v-model="config.target_area_y"
                    class="w-6 ml-2  text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary"
                    placeholder="坐标Y">
            </div>
        </div>

        <div class="w-full mt-4">
            <Button class="w-full justify-content-center" size="small" @click="navigateToTarget">
                <div>STEP1&nbsp;&nbsp;设置目标区域坐标</div>
            </Button>
        </div>

        <!-- 加载目标区域 -->
        <div class="w-full mt-4">
            <div class="flex h-13rem bg-primary border-round align-items-center justify-content-center">
                <div v-if="imgLoading" class="flex justify-content-center align-items-center"><i class="pi pi-spin pi-spinner mr-2"></i>获取图片中...</div>
                <cropper v-if="!imgLoading" ref="cropperView" :src="img" :stencil-props="{}" @change="change" />
            </div>
        </div>

        <!-- <div class="w-full mt-4 flex justify-content-between">
            <Button class="w-full justify-content-center" size="small">
                <div>STEP2&nbsp;&nbsp;导航到目标区域并选择目标</div>
            </Button>
        </div> -->

        <!-- 设置检测区域坐标 -->
        <div class="flex mt-4 w-full  align-items-center">
            <div class="flex w-6 justify-content-between align-items-center">
                <label class="w-6">检测框X</label>
                <input type="text" v-model="config.detect_region_x"
                    class="w-6 ml-2 mr-2 text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary"
                    placeholder="坐标X">
            </div>
            <div class="flex w-6 justify-content-between align-items-center">
                <label class="w-6 ml-2">检测框Y</label>
                <input type="text" v-model="config.detect_region_y"
                    class="w-6 ml-2  text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary"
                    placeholder="坐标Y">
            </div>
        </div>
        <div class="flex mt-4 w-full  align-items-center">
            <div class="flex w-6 justify-content-between align-items-center">
                <label class="w-6">检测框W</label>
                <input type="text" v-model="config.detect_region_w"
                    class="w-6 ml-2 mr-2 text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary"
                    placeholder="坐标X">
            </div>
            <div class="flex w-6 justify-content-between align-items-center">
                <label class="w-6 ml-2">检测框H</label>
                <input type="text" v-model="config.detect_region_h"
                    class="w-6 ml-2  text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary"
                    placeholder="坐标Y">
            </div>
        </div>

        <!-- 设置坐标 -->
        <div class="flex mt-4 w-full  align-items-center">
            <label class="w-6">检测周期(单位:秒)</label>
            <input type="text" v-model="config.protected_mask_query_time"
                class="w-6 text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary"
                placeholder="检测周期(s)">
        </div>

        <div class="w-full mt-4">
            <Button class="w-full justify-content-center" size="small" @click="saveConfig">
                <div>STEP2&nbsp;&nbsp;保存配置</div>
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
import { Cropper } from 'vue-advanced-cropper'
import 'vue-advanced-cropper/dist/style.css';
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';

const config = ref({
    target_area_x: 21,
    target_area_y: 73,
    detect_region_x: 0,
    detect_region_y: 0,
    detect_region_w: 80,
    detect_region_h: 80,
    protected_mask_query_time: 60,
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

function getConfig() {
    fetch("http://localhost:8000/devices/config", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    }).then((response) => {
        return response.json();
    }).then((data) => {
        if (data.data.protected_mask_region !== undefined) {
            var region = data.data.protected_mask_region[0]
            console.log("region", region !== undefined)
            if (region !== undefined) {
                config.value.target_area_x = region[0][0]
                config.value.target_area_y = region[0][1]
                config.value.detect_region_x = region[1][0]
                config.value.detect_region_y = region[1][1]
                config.value.detect_region_w = region[1][2]
                config.value.detect_region_h = region[1][3]
                cropperView.value.setCoordinates(({ coordinates, imageSize }) => ({
                    top: config.value.detect_region_y,
                    left: config.value.detect_region_x,
                    width: config.value.detect_region_w,
                    height: config.value.detect_region_h,
                }))
            }
        }
        if (data.data.protected_mask_query_time !== undefined) {
            config.value.protected_mask_query_time = data.data.protected_mask_query_time
        }
    }).catch((error) => {
        toast.add({ severity: 'error', summary: '获取配置失败', detail: error.message, life: 3000  });
    });
}

function navigateToTarget() {
    imgLoading.value = true;
    fetch("http://localhost:8000/devices/navigate?target_x="+config.value.target_area_x + "&target_y=" + config.value.target_area_y, {
        method: "GET"
    }).then((response) => {
        return response.json();
    }).then((data) => {
        if (data.status_code === 200) {
            imgLoading.value = false;
            toast.add({ severity: 'success', summary: '导航到目标区域成功', detail: data.message, life: 3000  });
        } else {
            toast.add({ severity: 'error', summary: '导航到目标区域失败', detail: data.message, life: 3000  });
        }
    }).catch((error) => {
        toast.add({ severity: 'error', summary: '导航到目标区域失败', detail: error.message, life: 3000  });
    });
}

function saveConfig() {
    fetch("http://localhost:8000/update/protect_config", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            index: 0,
            protected_mask_region: [[config.value.target_area_x, config.value.target_area_y], [config.value.detect_region_x, config.value.detect_region_y, config.value.detect_region_w, config.value.detect_region_h]],
            protected_mask_query_time: config.value.protected_mask_query_time
        })
    }).then((response) => {
        return response.json();
    }).then((data) => {
        if (data.status_code === 200) {
            toast.add({ severity: 'success', summary: '保存配置成功', detail: data.message, life: 3000  });
        } else {
            toast.add({ severity: 'error', summary: '保存配置失败', detail: data.message, life: 3000  });
        }
    }).catch((error) => {
        toast.add({ severity: 'error', summary: '保存配置失败', detail: error.message, life: 3000  });
    });
}

onMounted(() => {
    getConfig();
})

</script>