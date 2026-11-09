<template>
  <div class="min-h-screen bg-white relative">
    <!-- Header/Navbar -->
    <div class="flex items-center justify-between px-10 py-5 border-b border-gray-200">
      <div class="flex items-center space-x-3">
        <div class="w-9 h-9 bg-black rounded-full flex items-center justify-center">
          <span class="text-white text-xs font-bold">TG</span>
        </div>
        <span class="text-base font-semibold text-gray-900">TeamChem</span>
      </div>

      <nav class="flex space-x-8 text-sm">
        <router-link to="/" class="text-gray-600 hover:text-black transition">
          Home
        </router-link>

        <router-link
          to="/results"
          class="text-black font-semibold border-b-2 border-black pb-1"
        >
          Search
        </router-link>

        <router-link to="/history" class="text-gray-600 hover:text-black transition">
          History
        </router-link>
      </nav>
    </div>

    <!-- Main Content -->
    <div
      class="pt-14 pb-24 flex flex-col lg:flex-row items-start justify-start px-10 lg:px-16 space-y-16 lg:space-y-0 lg:space-x-20"
    >
      <!-- Left Side - Molecule Image (Sticky) -->
      <div class="flex-shrink-0 w-full max-w-sm lg:w-96 lg:sticky lg:top-28">
        <img
          src="/molekul.png"
          class="w-full h-auto object-contain drop-shadow-md"
          alt="Molecule"
        />
      </div>

      <!-- Right Side -->
      <div class="w-full flex-1 max-w-6xl">
        <div class="mb-12">
          <h1 class="text-4xl font-bold text-gray-900 tracking-tight">Recommendations</h1>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="text-center py-16">
          <p class="text-gray-600 text-lg">Loading recommendations...</p>
        </div>

        <!-- Empty -->
        <div v-else-if="recommendations.length === 0" class="text-center py-16">
          <p class="text-gray-600 text-lg">Tidak ada rekomendasi yang cocok.</p>
          <router-link
            to="/"
            class="text-blue-600 hover:underline mt-4 inline-block text-sm"
          >
            Kembali ke pencarian
          </router-link>
        </div>

        <!-- Cards -->
        <div
          v-else
          class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-10"
        >
          <div
            v-for="(item, index) in recommendations"
            :key="index"
            class="bg-white border border-gray-200 rounded-xl p-6 flex flex-col items-center hover:shadow-xl transition-shadow duration-300"
          >
            <!-- Molecule Image -->
            <div
              class="w-full h-48 bg-gray-50 flex items-center justify-center rounded-lg mb-5 border border-gray-200"
            >
              <img
                v-if="item.image"
                :src="item.image"
                alt="Molecule Structure"
                class="object-contain h-full w-full p-4"
              />
              <div v-else class="text-gray-400 text-sm">No Image Available</div>
            </div>

            <!-- SMILES -->
            <div class="w-full text-center mb-5 px-2">
              <p class="text-sm text-gray-700 font-mono break-all leading-relaxed">
                {{ item.smiles }}
              </p>
            </div>

            <!-- Button -->
            <button
              @click="goToDetail(item)"
              class="w-full bg-black text-white px-5 py-3 rounded-md text-sm font-semibold hover:bg-gray-800 active:bg-gray-900 transition"
            >
              View Detail
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter, useRoute } from "vue-router";
import { ref, onMounted } from "vue";

const router = useRouter();
const route = useRoute();

const recommendations = ref([]);
const loading = ref(false);

onMounted(() => {
  console.log("Resultpage mounted");
  console.log("Route params:", route.params);
  console.log("Route query:", route.query);

  let raw = route.params.results || route.query.results || null;

  if (!raw) {
    console.log("No data found in route");
    return;
  }

  try {
    const parsed = JSON.parse(raw);
    parsed.forEach((item) => {
      if (item.image && !item.image.startsWith("data:image")) {
        item.image = "data:image/png;base64," + item.image;
      }
    });

    recommendations.value = parsed;
  } catch (err) {
    console.error("Error parsing results:", err);
  }
});

function goToDetail(item) {
  sessionStorage.setItem("selectedCompound", JSON.stringify(item));
  router.push({
    path: "/detail",
    query: { smiles: item.smiles },
  });
}
</script>
