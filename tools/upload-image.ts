#!/usr/bin/env bun

import OSS from 'ali-oss';
import { existsSync } from 'fs';
import { basename, extname } from 'path';

// 检查环境变量
const requiredEnvVars = [
  'OSS_ACCESS_KEY_ID',
  'OSS_ACCESS_KEY_SECRET',
  'OSS_BUCKET',
  'OSS_REGION'
];

const missingVars = requiredEnvVars.filter(v => !process.env[v]);
if (missingVars.length > 0) {
  console.error('\n❌ 缺少必需的环境变量:');
  missingVars.forEach(v => console.error(`   - ${v}`));
  console.error('\n请复制 .env.example 为 .env 并填写正确的配置\n');
  process.exit(1);
}

// 获取命令行参数
const imagePath = process.argv[2];

if (!imagePath) {
  console.error('\n用法: bun run upload <图片路径>');
  console.error('示例: bun run upload ~/Downloads/screenshot.png\n');
  process.exit(1);
}

// 检查文件是否存在
if (!existsSync(imagePath)) {
  console.error(`\n❌ 文件不存在: ${imagePath}\n`);
  process.exit(1);
}

// 初始化 OSS 客户端
const client = new OSS({
  region: process.env.OSS_REGION!,
  accessKeyId: process.env.OSS_ACCESS_KEY_ID!,
  accessKeySecret: process.env.OSS_ACCESS_KEY_SECRET!,
  bucket: process.env.OSS_BUCKET!
});

// 生成时间戳格式的文件名
function generateFileName(originalPath: string): string {
  const ext = extname(originalPath);
  const now = new Date();

  // 格式: YYYY-MM-DD-HHMMSS.ext
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const seconds = String(now.getSeconds()).padStart(2, '0');

  return `${year}-${month}-${day}-${hours}${minutes}${seconds}${ext}`;
}

// 上传图片
async function uploadImage() {
  try {
    const fileName = generateFileName(imagePath);

    console.log(`\n📤 正在上传图片...`);
    console.log(`   文件: ${basename(imagePath)}`);
    console.log(`   目标: ${fileName}`);

    const result = await client.put(fileName, imagePath);

    // 生成 URL
    const url = process.env.OSS_CUSTOM_DOMAIN
      ? `${process.env.OSS_CUSTOM_DOMAIN}/${fileName}`
      : result.url.replace('http://', 'https://');

    // 输出 markdown 格式
    const markdown = `![](${url})`;

    console.log('\n✅ 上传成功!');
    console.log(`\n复制下面的内容到博客中:\n`);
    console.log(`${markdown}\n`);

    // 也输出纯 URL 方便其他用途
    console.log(`图片 URL: ${url}\n`);

  } catch (error) {
    console.error('\n❌ 上传失败:', error);
    process.exit(1);
  }
}

// 执行上传
uploadImage();
