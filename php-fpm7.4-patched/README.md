# PHP 7.4.33-FPM PHP2Shell backport

以官方 PHP 7.4.33 原始碼及官方 security commit 重編完整 CLI/FPM 基底，供上層 PHP 7.4 映像使用。

| 項目 | 固定版本／來源 |
| --- | --- |
| PHP | 7.4.33 |
| CVE | CVE-2026-109618、CVE-2026-109619 |
| 官方安全 commit | [`712e60f9edfd03f0960fc4fc3c2c375f42b90aa2`](https://github.com/php/php-src/commit/712e60f9edfd03f0960fc4fc3c2c375f42b90aa2) |
| 官方 Docker 配方／helpers | [`b9f17156020c3aef71df681b27684533529347a7`](https://github.com/docker-library/php/tree/b9f17156020c3aef71df681b27684533529347a7/7.4/bullseye/fpm) |
| Debian 基底 | `bullseye-slim@sha256:e5b6442dd2e9684cf5e87d8338b5968f3b348636fc0be6d7850a381e3731a2bd` |

這是 PHP 官方標為 **Minimal mitigation for EOL version** 的回移植。它有兩項應用可見的行為：

- OOM 時直接結束 worker，不執行 PHP shutdown callback；FPM 會補建 worker。
- Session upload progress 在 C 層停用；即使 INI 重新設定為開啟也不會恢復功能。

另外設定 `session.upload_progress.enabled=Off`。不能將這個 INI 設定視為兩個 CVE 的完整修補。此次回移植也不代表 PHP 7.4、Debian Bullseye 或上層 extensions 的完整安全維護。

## 建置與測試

需要 Python 3、Docker Engine 與 buildx。在本目錄執行：

```sh
./build.sh
./test.sh
./phpt.sh
```

`build.sh` 會先驗證 `sources.lock.json` 中的輸入；缺少的檔案由固定 HTTPS 來源下載並核對 SHA256。PHP 壓縮檔不放進 Git。PEAR／PECL channel XML 隨版本固定並校驗，避免即時 metadata 端點偶發回傳錯誤內容造成編譯後失敗。已有檔案若校驗失敗，程式會停止，不會覆寫。

預設本機 tag：`php74-fpm-patched:7.4.33-php2shell-712e60f9edfd`。預設採 Docker daemon 的原生 arm64 或 amd64 架構；亦可明確指定：

```sh
PLATFORM=linux/amd64 PHP74_IMAGE=php74-fpm-patched:amd64-check ./build.sh
PHP74_IMAGE=php74-fpm-patched:amd64-check ./test.sh
PHP74_IMAGE=php74-fpm-patched:amd64-check ./phpt.sh
```

指定的架構必須能在測試主機執行；不要將 cross-build 成功當成目標平台驗證通過。

如需自行執行 `docker build`，必須先準備完整建置目錄：

```sh
python3 fetch-inputs.py
docker build -t php74-fpm-patched:local .
```

直接指定遠端 Dockerfile 不會自動執行 `fetch-inputs.py`。本目錄的 `Dockerfile` 需要壓縮檔、`security.patch` 及 `docker-php-*` helpers 同時存在於 build context。

## 自動驗證

[`php74-patched.yml`](../.github/workflows/php74-patched.yml) 在 GitHub 原生 arm64 / amd64 runner 上分別建置及測試，保留每個架構的報告 artifact。此流程不登入 registry、不推送 Docker Hub，也不執行部署。

驗收包括：

- CLI/FPM/phpize/php-config 及 FPM 設定檢查。
- 17 個修補檔案的 hash 與固定官方 commit 的完整檔案一致。
- OOM 不執行 shutdown callback、FPM 補建 worker。
- 同一個非 root worker 連續處理 fatal error，再處理帶早期 INI diagnostic 的請求。
- Multipart upload progress 即使被 INI 重新開啟，仍不產生進度 session。
- 官方選定的 array、generator、exception、session encode/decode PHPT。

報告寫入本目錄 `reports/`，包含命令、exit code、image ID、binary hashes 和測試輸出。測試使用 `--network none` 的 disposable container，沒有掛載主機資料或發布 host port。

官方安全 commit 沒有附 CVE 專用 PHPT；以上結合原始碼、產物及限定 lifecycle 測試，不宣稱完整 exploit reproduction 或涵蓋所有 extension producer/consumer。

## 上層映像與發布

保留官方 `docker-php-ext-*`、`docker-php-source`、phpize、php-config、headers、FPM 設定、entrypoint、UID/GID 33、9000 及 SIGQUIT 等介面。上層 native extensions 必須針對新基底重新編譯與驗證。

發布時使用新版本 tag，驗收後再推送到操作者明確確認的 registry repository。上層 `FROM` 應固定為發布後查到的遠端 manifest digest。這裡沒有預設 Docker Hub namespace，也不覆蓋 `latest`。

正式應用相容性、外部資料庫／快取／搜尋服務整合，以及其他 EOL 漏洞，需要另外驗證。

## 來源與授權

詳見 [PATCH_PROVENANCE.md](PATCH_PROVENANCE.md)、[VALIDATION.md](VALIDATION.md) 及 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
