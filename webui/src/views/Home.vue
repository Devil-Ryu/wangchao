<template>

    <div class="h-full flex flex-column bg-gray-300">
        <div class="flex justify-content-center align-items-center h-12rem bg-primary border-round m-2 ">信息展示</div>
        <div class="h-full m-2">
            <div class="flex bg-primary w-full border-round  align-items-center h-4rem">
                <div id="icon" class="flex  h-full  w-4rem align-items-center justify-content-center"><i
                        class="pi pi-th-large" style="font-size: 1.5rem;"></i></div>
                <div class="w-full h-full  flex justify-content-between align-items-center">
                    <div class="ml-2">测试功能一</div>
                    <div class="flex">
                        <Button >配置</Button>
                        <Button >启用</Button>
                    </div>
                </div>

            </div>
            <div class="flex  bg-primary w-full border-round  align-items-center h-4rem mt-2">
                <div id="icon" class="flex  h-full  w-4rem align-items-center justify-content-center"><i
                        class="pi pi-th-large" style="font-size: 1.5rem;"></i></div>
                <div class="w-full h-full  flex justify-content-between align-items-center">
                    <div class="ml-2">测试功能二</div>
                    <div class="flex">
                        <Button >配置</Button>
                        <Button >启用</Button>
                    </div>
                </div>

            </div>
        </div>
        <!-- <TabMenu :model="items" /> -->
    </div>


</template>

<script setup>
import { ref } from 'vue';
const options = [
    { name: 'Option 1', value: 1 },
    { name: 'Option 2', value: 2 },
    { name: 'Option 3', value: 3 },
    { name: 'Option 4', value: 4 },
];


const items = ref([
    {
        label: '功能一',
        icon: 'pi pi-refresh'
    },
    {
        label: '功能二',
        icon: 'pi pi-upload'
    }

]);

const toggle = (event) => {
    menu.value.toggle(event);
};

function handleSelect({ originalEvent, value }) {
    console.log("selected originalEvent: ", originalEvent);
    console.log("selected value: ", value);
}

</script>

<style scoped></style>