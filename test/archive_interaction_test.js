const assert = require("assert");
const { selectVisibleItems } = require("../assets/js/archive");

const items = [
  { year: "2026", channel: "tech", tags: ["AI", "系统"] },
  { year: "2026", channel: "life", tags: ["湾区"] },
  { year: "2011", channel: "legacy", tags: ["C++"] },
  { year: "2011", channel: "tech", tags: ["系统"] },
];

assert.deepStrictEqual(selectVisibleItems(items, {}, 2), {
  matchingIndexes: [0, 1, 2, 3],
  visibleIndexes: [0, 1],
});

assert.deepStrictEqual(selectVisibleItems(items, { channel: "tech" }, 20), {
  matchingIndexes: [0, 3],
  visibleIndexes: [0, 3],
});

assert.deepStrictEqual(selectVisibleItems(items, { year: "2011", tag: "系统" }, 20), {
  matchingIndexes: [3],
  visibleIndexes: [3],
});

console.log("archive interactions: ok");
