(function (root) {
  "use strict";

  function selectVisibleItems(items, filters, limit) {
    var year = filters.year || "";
    var channel = filters.channel || "";
    var tag = filters.tag || "";
    var matchingIndexes = [];

    items.forEach(function (item, index) {
      var tags = Array.isArray(item.tags) ? item.tags : [];
      if (year && item.year !== year) return;
      if (channel && item.channel !== channel) return;
      if (tag && tags.indexOf(tag) === -1) return;
      matchingIndexes.push(index);
    });

    return {
      matchingIndexes: matchingIndexes,
      visibleIndexes: matchingIndexes.slice(0, limit),
    };
  }

  function readTags(element) {
    try {
      return JSON.parse(element.getAttribute("data-tags") || "[]");
    } catch (_error) {
      return [];
    }
  }

  function enhanceArchive(element) {
    var itemElements = Array.prototype.slice.call(element.querySelectorAll("[data-archive-item]"));
    var items = itemElements.map(function (item) {
      return {
        year: item.getAttribute("data-year") || "",
        channel: item.getAttribute("data-channel") || "legacy",
        tags: readTags(item),
      };
    });
    var yearSelect = element.querySelector("[data-archive-year]");
    var channelSelect = element.querySelector("[data-archive-channel]");
    var loadMore = element.querySelector("[data-archive-load-more]");
    var count = element.querySelector("[data-archive-count]");
    var empty = element.querySelector("[data-archive-empty]");
    var activeTag = element.querySelector("[data-archive-active-tag]");
    var batchSize = Number(element.getAttribute("data-batch-size")) || 20;
    var visibleLimit = batchSize;
    var query = new URLSearchParams(root.location.search);
    var tag = query.get("tag") || "";

    if (tag && activeTag) {
      activeTag.textContent = "标签：" + tag;
      activeTag.hidden = false;
    }

    function render() {
      var result = selectVisibleItems(items, {
        year: yearSelect ? yearSelect.value : element.getAttribute("data-fixed-year") || "",
        channel: channelSelect ? channelSelect.value : "",
        tag: tag,
      }, visibleLimit);
      var visible = new Set(result.visibleIndexes);
      var matching = new Set(result.matchingIndexes);

      itemElements.forEach(function (item, index) {
        item.hidden = !matching.has(index) || !visible.has(index);
      });

      if (count) count.textContent = "显示 " + result.visibleIndexes.length + " / " + result.matchingIndexes.length + " 篇";
      if (empty) empty.hidden = result.matchingIndexes.length !== 0;
      if (loadMore) loadMore.hidden = result.visibleIndexes.length >= result.matchingIndexes.length;
      element.classList.add("is-ready");
    }

    function resetAndRender() {
      visibleLimit = batchSize;
      render();
    }

    if (yearSelect) yearSelect.addEventListener("change", resetAndRender);
    if (channelSelect) channelSelect.addEventListener("change", resetAndRender);
    if (loadMore) {
      loadMore.addEventListener("click", function () {
        visibleLimit += batchSize;
        render();
      });
    }
    render();
  }

  var api = { selectVisibleItems: selectVisibleItems };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  if (root && root.document) {
    root.ArchiveInteractions = api;
    root.document.addEventListener("DOMContentLoaded", function () {
      Array.prototype.forEach.call(root.document.querySelectorAll("[data-archive]"), enhanceArchive);
    });
  }
})(typeof window !== "undefined" ? window : {});
