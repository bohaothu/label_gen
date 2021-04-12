<template>
  <div>
    <v-snackbar v-model="$store.state.snackbar.status">{{$store.state.snackbar.msg}}
    </v-snackbar>
  </div>
</template>

<script>
export default {
  name: 'GlobalSnackBar'
}
</script>