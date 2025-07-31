# CampySer - 空肠弯曲菌血清分型工具

CampySer 是一个基于BLAST的空肠弯曲菌血清分型命令行工具，能够快速分析FASTA格式的基因组序列并预测其血清型。

## 功能特点

- 🧬 **快速血清分型**: 基于BLAST算法对空肠弯曲菌进行血清型预测
- 📊 **详细分析报告**: 提供相似度、覆盖度、E值等详细的比对统计信息
- 🎯 **高精度识别**: 使用严格的筛选阈值确保结果准确性
- 🔧 **易于使用**: 简单的命令行界面，支持多种输出格式
- 📈 **可视化输出**: 支持详细模式和简洁模式的输出

## 系统要求

### 必需软件
- **Python 3.6+**: [下载Python](https://www.python.org/downloads/)
- **BLAST+ 2.12.0+**: [下载BLAST+](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download)

### 安装BLAST+
```bash
# mamba
mamba install blast -c bioconda

# 或者从NCBI官网下载
wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.12.0+-x64-linux.tar.gz
tar -xvzf ncbi-blast-2.12.0+-x64-linux.tar.gz
export PATH=$PATH:$(pwd)/ncbi-blast-2.12.0+/bin
```

## 安装 CampySer

### 1. 克隆仓库
```bash
git clone https://github.com/yourusername/CampySer.git
cd CampySer
```

### 2. 下载序列数据
```bash
python download_sequences.py
```

### 3. 构建BLAST数据库
```bash
# 构建主数据库
makeblastdb -in sequences/all_sequences.fasta -dbtype nucl -out database/campylobacter_db
```

## 使用方法

### 基本用法
```bash
python campyser.py contigs.fasta
```

### 详细输出模式
```bash
python campyser.py contigs.fasta --verbose
```

### 保存结果到文件
```bash
python campyser.py contigs.fasta --output results.txt
```

### 指定自定义数据库路径
```bash
python campyser.py contigs.fasta --database /path/to/your/database
```

### 完整参数选项
```bash
usage: campyser.py [-h] [--output OUTPUT] [--verbose] [--database DATABASE] fasta_file

Campylobacter Serotyping Analysis Tool

positional arguments:
  fasta_file            Input FASTA file to analyze

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        Output file for results (default: stdout)
  --verbose, -v         Verbose output
  --database DATABASE, -d DATABASE
                        BLAST database path (default: database/campylobacter_db)
```

## 输出结果解读

### 标准输出
```
Predicted Serotype: HS2
Confidence: High
Method: BLAST
Identity: 97.0%
Coverage: 100.0%
```

### 详细输出 (--verbose)
```
Analysis completed for: contigs.fasta
Database: database/campylobacter_db
--------------------------------------------------
BLAST结果排序后的前五行信息:
--------------------------------------------------------------------------------
序列ID                 比对序列            一致性        覆盖度        E值           比特分数      
--------------------------------------------------------------------------------
1                    CP000025.1      88.0       13.4       0.00e+00     41842.0   
2                    AL111168.1      87.9       13.4       0.00e+00     41643.0   
3                    CP000025.1      85.6       13.7       0.00e+00     37824.0   
4                    AL111168.1      85.6       13.7       0.00e+00     37807.0   
5                    CP000025.1      87.0       9.6        0.00e+00     33576.0   

Predicted Serotype: HS2
Confidence: High
Method: BLAST
Identity: 97.0%
Coverage: 100.0%

Detailed Results:
------------------------------
BLAST Results:
  1. HS2 (AL111168.1)
     Identity: 97.0%, Coverage: 100.0%
     E-value: 0.00e+00
  2. HS53 (CP000025.1)
     Identity: 88.0%, Coverage: 13.4%
     E-value: 0.00e+00
  3. HS53 (CP000025.1)
     Identity: 85.6%, Coverage: 13.7%
     E-value: 0.00e+00
```

### 结果字段说明
- **Predicted Serotype**: 预测的血清型
- **Confidence**: 置信度 (High/Medium/Low)
- **Method**: 分析方法 (BLAST)
- **Identity**: 序列相似度百分比
- **Coverage**: 覆盖度百分比
- **E-value**: 期望值，越小越好
- **Bitscore**: 比特分数，越高越好

## 支持的血清型

当前版本支持以下空肠弯曲菌血清型：

| 血清型 | 登录号 | 描述 |
|--------|--------|------|
| HS1 | BX545859 | 空肠弯曲菌HS1血清型 |
| HS2 | AL111168.1 | 空肠弯曲菌HS2血清型 |
| HS3 | HQ343268 | 空肠弯曲菌HS3血清型 |
| HS4 | HQ343269 | 空肠弯曲菌HS4血清型 |
| HS6 | NC_009839 | 空肠弯曲菌HS6血清型 |
| HS8 | HQ343270 | 空肠弯曲菌HS8血清型 |
| HS10 | HQ343271 | 空肠弯曲菌HS10血清型 |
| HS15 | HQ343272 | 空肠弯曲菌HS15血清型 |
| HS17 | HQ343273 | 空肠弯曲菌HS17血清型 |
| HS19 | BX545860 | 空肠弯曲菌HS19血清型 |
| HS23 | AY332625 | 空肠弯曲菌HS23血清型 |
| HS36 | AY332624 | 空肠弯曲菌HS36血清型 |
| HS41 | BX545857 | 空肠弯曲菌HS41血清型 |
| HS42 | HQ343274 | 空肠弯曲菌HS42血清型 |
| HS53 | CP000025.1 | 空肠弯曲菌HS53血清型 |

## 项目结构

```
CampySer/
├── campyser.py              # 主程序文件
├── download_sequences.py    # 序列下载脚本
├── test_blast_top5.py       # BLAST测试脚本
├── ser_an.txt               # 血清型映射文件
├── contigs.fasta           # 示例输入文件
├── database/               # BLAST数据库目录
│   ├── campylobacter_db.nhr
│   ├── campylobacter_db.nin
│   ├── campylobacter_db.nsq
│   └── ...
├── sequences/              # 参考序列目录
│   ├── HS1.fasta
│   ├── HS2.fasta
│   ├── HS3.fasta
│   └── ...
├── README.md               # 项目说明文档
└── CLAUDE.md               # 开发指导文档
```

## 工作原理

1. **序列比对**: 使用BLASTn算法将输入序列与参考数据库进行比对
2. **结果筛选**: 应用严格的筛选标准：
   - 序列相似度 ≥ 95%
   - 覆盖度 ≥ 80%
   - E值 ≤ 1e-10
3. **血清型预测**: 根据最佳匹配的登录号确定血清型
4. **置信度评估**: 基于比对质量分配置信度等级

## 故障排除

### 常见问题

#### 1. "blastn not found" 错误
**问题**: 程序无法找到BLAST+工具
**解决**: 确保BLAST+已正确安装并添加到系统PATH中

```bash
# 检查BLAST是否安装
blastn -version

# 如果未安装，请参考上面的安装说明
```

#### 2. "No serotype detected" 结果
**问题**: 程序未检测到血清型
**可能原因**:
- 输入序列质量较差
- 序列与数据库中的参考序列相似度不足
- 序列长度太短

**解决**:
- 检查输入FASTA文件格式是否正确
- 使用`--verbose`参数查看详细的BLAST结果
- 考虑降低筛选阈值（需要修改代码）

#### 3. 数据库文件不存在
**问题**: 程序提示数据库文件不存在
**解决**: 重新构建BLAST数据库

```bash
# 确保序列文件存在
ls sequences/all_sequences.fasta

# 重新构建数据库
makeblastdb -in sequences/all_sequences.fasta -dbtype nucl -out database/campylobacter_db
```

#### 4. 权限问题
**问题**: 无法写入输出文件
**解决**: 检查文件权限或使用不同的输出路径

```bash
# 检查当前目录权限
ls -la

# 使用有写权限的目录
python campyser.py contigs.fasta --output /tmp/results.txt
```

### 调试模式

使用详细输出模式获取更多信息：
```bash
python campyser.py contigs.fasta --verbose
```

## 性能优化

### 大文件处理
对于大型基因组文件，建议：
1. 使用足够的内存（建议8GB以上）
2. 在SSD上运行程序
3. 考虑分批处理大型文件

### 数据库优化
定期更新参考序列数据库：
```bash
# 更新序列
python download_sequences.py

# 重新构建数据库
makeblastdb -in sequences/all_sequences.fasta -dbtype nucl -out database/campylobacter_db
```

## 开发和贡献

### 代码结构
- `CampySerAnalyzer`: 主要的分析类
- `_load_serotype_mapping()`: 加载血清型映射
- `run_blast_analysis()`: 执行BLAST分析
- `_parse_blast_results()`: 解析BLAST结果
- `interpret_results()`: 解释结果并预测血清型

### 添加新的血清型
1. 在`ser_an.txt`中添加新的血清型映射
2. 下载相应的参考序列到`sequences/`目录
3. 重新构建BLAST数据库

### 自定义阈值
可以在代码中修改以下参数：
- `identity`阈值 (默认: 95%)
- `coverage`阈值 (默认: 80%)
- `evalue`阈值 (默认: 1e-10)

## 许可证

本项目采用MIT许可证。详情请参见LICENSE文件。

## 引用

如果您在研究中使用了CampySer，请引用：

```
CampySer: A BLAST-based Campylobacter serotyping tool
Version 1.0
https://github.com/yourusername/CampySer
```
## 参考文献
《Updated Campylobacter jejuni Capsule PCR Multiplex Typing System and Its Application to Clinical Isolates from South and Southeast Asia》(https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0144349)

## 更新日志

### v1.0.0 (2024-01-01)
- 初始版本发布
- 支持19种空肠弯曲菌血清型
- 基于BLAST的血清分型算法
- 命令行界面和详细输出模式

---

**注意**: 本工具仅用于研究目的。在实际临床应用中，请结合其他实验室方法进行验证。
