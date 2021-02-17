<template>
  <div>
    <Sidebar />
    <Datatable/>
  </div>
</template>
<script>
import Datatable from '../components/Datatable'
import Sidebar from '../components/Sidebar'

export default {
  components:{
    Datatable,
    Sidebar
  }
}
</script>