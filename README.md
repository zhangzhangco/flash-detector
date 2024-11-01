# 视频闪光检测工具 (Video Flash Detector)

一个基于Python的视频闪光检测工具，可以自动识别视频中的闪光序列，支持命令行和图形界面两种使用方式。

## 功能特点

- 🎯 准确检测视频中的闪光序列
- 🖼️ 支持多种可视化方式（原始帧、热力图、区域放大）
- 🔄 使用环形缓冲区实现实时检测
- 📊 提供详细的检测结果和性能统计
- 🎛️ 丰富的参数调整选项
- 💻 同时支持命令行和GUI界面

## 安装方法

### 环境要求
- Python 3.8+
- OpenCV 4.5+
- NumPy 1.19+
- Gradio 3.x
- psutil 5.8+
- pytest 6.0+ (用于开发)

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/yourusername/flash_detector.git
cd flash_detector
```
2. 创建虚拟环境（推荐）
```bash
python -m venv venv
source venv/bin/activate # Linux/Mac
```
或
```bash
venv\Scripts\activate # Windows
```
3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 安装项目
```bash
pip install -e .
```

## 使用方法

### 命令行模式

基本使用：
```bash
python -m flash_detector video_path [options]
```

完整参数说明：
参数：
video_path 视频文件路径
--abs_threshold 绝对差异阈值 (默认: 20)
--rel_threshold 相对变化阈值 (默认: 0.3)
--region_size 检测区域大小 (默认: 20)
--frame_step 帧比较步长 (默认: 1)
--start_time 开始时间 (默认: "0:00")
--circularity_threshold 圆形度阈值 (默认: 0.5)

示例：
基本使用
```bash
python -m flash_detector video.mp4
```
调整参数
```bash
python -m flash_detector video.mp4 --abs_threshold 15 --rel_threshold 0.25
```
指定开始时间
```bash
python -m flash_detector video.mp4 --start_time "1:30"
```
### 图形界面模式

启动GUI：
```bash
python -m flash_detector
```
### Python API使用

```python
from flash_detector.core.detector import detect_flash
```
检测视频中的闪光
```python
results = detect_flash(
video_path="video.mp4",
abs_threshold=20,
rel_threshold=0.3,
region_size=20,
frame_step=1,
start_time="0:00",
circularity_threshold=0.5
)
```
处理结果
```python
if results:
flash_info, debug_images = results
frame_num, intensity, position = flash_info
print(f"检测到闪光：帧号 {frame_num}, 强度 {intensity}, 位置 {position}")
```

## 参数调优建议

1. **绝对差异阈值** (15-25)
   - 较低：增加检测灵敏度，可能产生误报
   - 较高：减少误报，可能漏检
   - 建议值：20

2. **相对变化阈值** (0.3)
   - 较低（<0.3）：适合检测微弱闪光
   - 较高（>0.3）：只检测明显闪光
   - 建议值：0.3（表示30%变化）

3. **圆形度阈值** (0.5)
   - 较低：放宽形状限制
   - 较高：严格限制为圆形
   - 建议值：0.5-0.7

4. **检测区域大小** (20)
   - 较小（10-15）：适合小范围闪光
   - 较大（25-30）：适合大范围闪光
   - 建议值：20

## 性能基准测试

测试环境：
- CPU: Intel i7-9750H
- RAM: 16GB
- 视频分辨率: 1920x1080
- 帧率: 30fps

性能数据：
- 处理速度：约25-30fps
- 内存使用：~200MB
- CPU使用率：30-40%

## 常见问题 (FAQ)

1. **Q: 为什么检测不到闪光？**
   - A: 尝试降低绝对差异阈值（--abs_threshold）
   - A: 检查视频质量和闪光是否明显
   - A: 确保检测区域大小合适

2. **Q: 程序运行很慢？**
   - A: 增加帧步长（--frame_step）
   - A: 减小检测区域大小
   - A: 检查系统资源占用

3. **Q: 出现误报？**
   - A: 提高绝对差异阈值
   - A: 提高圆形度阈值
   - A: 增加相对变化阈值

## 开发指南

### 运行测试
安装开发依赖
```bash
pip install pytest
```
运行所有测试
```bash
pytest tests/
```
运行特定测试
```bash
pytest tests/test_detector.py
```

### 代码风格
- 遵循PEP 8规范
- 使用类型注解
- 添加详细的文档字符串

## 开发计划

- [ ] 支持批量视频处理
- [ ] 添加深度学习模型支持
- [ ] 优化检测速度
- [ ] 添加更多可视化选项
- [ ] 支持实时视频流处理
- [ ] 添加GUI配置保存功能

## 贡献指南

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

### 提交PR前检查清单
- [ ] 更新了文档
- [ ] 添加了测试用例
- [ ] 通过了所有测试
- [ ] 代码符合PEP 8规范

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 致谢

- OpenCV团队
- Gradio开发团队
- NumPy团队
- 所有贡献者

## 更新日志

### v1.0.0 (2024-10)
- 初始版本发布
- 支持GUI和命令行模式
- 实现基本的闪光检测功能
