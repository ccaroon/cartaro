<template>
  <!-- eslint-disable vue/no-v-text-v-html-on-component -->
  <span v-html="$markdown.render('# Debug\n > Dont Quote Me!')"></span>
</template>
