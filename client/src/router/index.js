import Vue from 'vue';
import VueRouter from 'vue-router';
import FileUploader from "../views/FileUploader";

Vue.use(VueRouter); //View Router를 사용했다고 선언

const router = new VueRouter({
    mode:"history",

    routes:[{
        path:"/", 
        component: FileUploader
    },
    ]
});

export default router;