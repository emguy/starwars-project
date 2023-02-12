<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
</script>

<style lang="scss">
@import "@/styles/app.scss";
@import "@/styles/_variables.scss";

#app {
  @include font-smoothing;
  font-family: $font-stack-sans;
}
</style>
