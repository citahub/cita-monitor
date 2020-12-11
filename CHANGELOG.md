# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [v0.6.0](https://github.com/citahub/cita-monitor/releases/tag/v0.6.0) ([compare](https://github.com/citahub/cita-monitor/compare/v0.5.0...v0.6.0))

### Changed
- Replace wget with curl to support socks5 protocol ([f1bd6d7](https://github.com/citahub/cita-monitor/commit/f1bd6d719e4af3511ea3d909725cd3c4f040c2d7) by wangpengfei).
- Update agent images to support arm64/amd64 ([5f5e812](https://github.com/citahub/cita-monitor/commit/5f5e8121cab1e97924af819ac0c12c0987383fb6) by wangpengfei).
- Upgrade images to support arm/arm64 ([8f33dcc](https://github.com/citahub/cita-monitor/commit/8f33dcc6633ee03b41d0413a2bfc59c060a779cf) by wangpengfei).
- Upgrade server images to support arm/arm64 ([0f10502](https://github.com/citahub/cita-monitor/commit/0f105025a5099467e827d1e140a5328f68fd80a6) by wangpengfei).

### Documented
- Update alert policies document ([50ca7ba](https://github.com/citahub/cita-monitor/commit/50ca7ba13124b1d6aaaae790daa5ce7afedf07c1) by RainChen).

### Fixed
- Fix make recipe: `make commit-release-notes` ([57568f7](https://github.com/citahub/cita-monitor/commit/57568f763b64258ebc35e090070a88625de60f51) by RainChen).


## [v0.5.0](https://github.com/citahub/cita-monitor/releases/tag/v0.5.0) ([compare](https://github.com/citahub/cita-monitor/compare/v0.4.1...v0.5.0)) - 2020-06-11

### Added
- Add dashboard language choices ([fec0975](https://github.com/citahub/cita-monitor/commit/fec0975f02b21693681d948f650d78f76abfdaff) by miaojun).
- Add disk alarm rules ([bd5f83d](https://github.com/citahub/cita-monitor/commit/bd5f83dfe5e06ad416cd29a515b8a7f8db2b9cad) by mfuuzy).
- Enable promethues configuration hot update function ([fc8d380](https://github.com/citahub/cita-monitor/commit/fc8d3801f564a0b99af58c746f47aea4638f9f71) by JiangXL).

### Changed
- Change the way to read node address ([233509a](https://github.com/citahub/cita-monitor/commit/233509a394d1940be2001646abba6bd542cf27b6) by miaojun).

### Documented
- Docs: fix outdated url in changelog.md ([0c93b5c](https://github.com/citahub/cita-monitor/commit/0c93b5c92dd6f8c478fdad8da97bbfee6d78fc37) by RainChen).
- Add multi language support explanation in readme.md ([37ea930](https://github.com/citahub/cita-monitor/commit/37ea930ea0d446e52fbe0777a7c08bcc22b93530) by miaojun).
- Update agent readme citamon/agent-cita-exporter port to 1923 ([3d54916](https://github.com/citahub/cita-monitor/commit/3d549160ecda0f907b71f89ec563648c9d2e6b50) by FengJunSun).
- Add bandit skip issue explanation ([bddf184](https://github.com/citahub/cita-monitor/commit/bddf184bfbfb8b4ab911a2204bbb6fa23ca62ad5) by miaojun).

### Fixed
- Fix cita_monitor_agent.py for hex_number initialization issue ([08b0c79](https://github.com/citahub/cita-monitor/commit/08b0c7940a1a9acba8e8bbc1aec66a14195a6ac9) by flyq).
- Fix security vulnerability in psutil ([20e3056](https://github.com/citahub/cita-monitor/commit/20e30564406848a1a3667fdb0192726cee4a6124) by miaojun).

### Misc
- Update copyright owner in license ([3169e20](https://github.com/citahub/cita-monitor/commit/3169e20be6d131a42b66abc27cf0ec7a7d75975e) by RainChen).
- Migrate repo from cryptape to citahub ([03a4ecd](https://github.com/citahub/cita-monitor/commit/03a4ecd219999fe149e4915a6ce6d65d0ee471f0) by RainChen).
- Show more padding for `make help` ([a755ea5](https://github.com/citahub/cita-monitor/commit/a755ea5b3e19e949dfbdfbba887c85e417f6d64d) by RainChen).
- Config bandit to skip some issues[b605,b607,b104] ([df78869](https://github.com/citahub/cita-monitor/commit/df788696d266dce63b8e99239e24986ab670d715) by miaojun).
- Use bandit as linter tool to find common security issues in python code ([45629cd](https://github.com/citahub/cita-monitor/commit/45629cd900c303899bf9ba52e90d51f33c014a64) by RainChen).


## [v0.4.1](https://github.com/citahub/cita-monitor/releases/tag/v0.4.1) ([compare](https://github.com/citahub/cita-monitor/compare/v0.4.0...v0.4.1)) - 2019-10-15

### Added
- Add: show rabbitmq-server process info in process info dashboard ([43d3e57](https://github.com/citahub/cita-monitor/commit/43d3e5763a522abfa06357e541056f494da8987b) by RainChen).

### Documented
- Docs: fix typo in release flow ([75bf6eb](https://github.com/citahub/cita-monitor/commit/75bf6ebd8cb876a23374ecbe7afcd1dfec61584c) by RainChen).

### Fixed
- Fix prometheus not connected due to incorrect container name alertmanager ([fd0b5b2](https://github.com/citahub/cita-monitor/commit/fd0b5b276cfef7f72491fa4887c974b7ff3eb662) by JiangXL).
- Fix live update of soft version ([0e9ea40](https://github.com/citahub/cita-monitor/commit/0e9ea402b8129944c9f4a27fb5d3b345780ffeff) by blankwu).

### Misc
- Refactor: format python codes ([3a83b26](https://github.com/citahub/cita-monitor/commit/3a83b262c4b6f415427002f6fd24ce83e67eaa0a) by RainChen).
- Change yapf/pylinctrc config with custom rules ([8d54754](https://github.com/citahub/cita-monitor/commit/8d54754e166bb6a2de57cd233f85b7b5bdab358e) by RainChen).


## [v0.4.0](https://github.com/citahub/cita-monitor/releases/tag/v0.4.0) ([compare](https://github.com/citahub/cita-monitor/compare/v0.3.0...v0.4.0)) - 2019-07-30

### Added
- Agent script gets block consensus node votes ([66dbeb7](https://github.com/citahub/cita-monitor/commit/66dbeb7683a46c8e204a87c884af19e74f5f2e75) by JiangXL).
- Control the execution frequency of the du command, once every 1 hour ([ffb1929](https://github.com/citahub/cita-monitor/commit/ffb192906ed3065396f0d371cb099fc9b744d509) by JiangXL).
- Add cita_with_agent to Integrate CITA with agent services ([8eeddbd](https://github.com/citahub/cita-monitor/commit/8eeddbd356ffd14e8dab04efc5004ab0a200ae8c) by mfuuzy).
- Add block consensus node vote number displayed in chain info ([757a20d](https://github.com/citahub/cita-monitor/commit/757a20d2e679622fc744153df83d3c0199775ed9) by JiangXL).
- Add a node directory log file using the size of the display ([e42ad5f](https://github.com/citahub/cita-monitor/commit/e42ad5f074047133c5a155885e2f06129fcc3018) by JiangXL).
- Add agent proxy to get data using one port ([c91946b](https://github.com/citahub/cita-monitor/commit/c91946ba61c5b787068fffe54c236d6f37cb4ebd) by JiangXL).
- Add test/makefile to bring in build/test recipes ([576d8c9](https://github.com/citahub/cita-monitor/commit/576d8c9de51c72cefb528197ef35a4916a441a15) by RainChen).
- Add test dir and init system testing env ([7c3b237](https://github.com/citahub/cita-monitor/commit/7c3b23746b8f388e0eca05833381c7db66b1f0f2) by RainChen).
- Add `make generate-build-version`: generate build metadata using format "x.y.z+yyyymmddhhmmss.commitshortid", e.g.: "0.3.0+20190606200449.40564fe"; add `make show-full-version`: show product version and build version, e.g.: "v0.3.0+20190606201137.40564fe" ([bcc76f9](https://github.com/citahub/cita-monitor/commit/bcc76f90e6bb64d84ba9d3bde4063e0067b022dc) by RainChen).
- Add genesis block hash display for chain meta data ([2d38c53](https://github.com/citahub/cita-monitor/commit/2d38c536b7e726ebec48fbb2539e1886948777e8) by JiangXL).
- Dashboard add version display ([99447fd](https://github.com/citahub/cita-monitor/commit/99447fd1e54f8220a68cc38d0d61cdbb29058a2a) by blankwu).


### Changed
- Change the service name ([a031404](https://github.com/citahub/cita-monitor/commit/a031404d7b22ca1f83363eacea19ba0614e57463) by mfuuzy).
- Update readme agent unified port ([9ccb065](https://github.com/citahub/cita-monitor/commit/9ccb0658dd691321d91f741fbdd12f5a4076e179) by JiangXL).
- Update test/makefile to add `make rpc-block-number-all` to call cita rpc method blocknumber for all nodes ([375eab4](https://github.com/citahub/cita-monitor/commit/375eab44a1e5795127f9e857f58e545af22a2aff) by RainChen).
- Update prometheus.yml for deployment only when you need to sed once ([c13611e](https://github.com/citahub/cita-monitor/commit/c13611e073060e074d4e800728430f3bc62cef00) by JiangXL).
- Update document instructions to modify the agent to expose only one port ([e0abb7b](https://github.com/citahub/cita-monitor/commit/e0abb7be03d3f0c850ff75994e641bb645f15b07) by JiangXL).
- Update grafana build process ([50311b5](https://github.com/citahub/cita-monitor/commit/50311b5c0ddcfca3bb0de326cae0338d00b342bc) by blankwu).
- Update grafana build process, del compose mount dashboard files ([d228c24](https://github.com/citahub/cita-monitor/commit/d228c2413a69669fe8adddcb544ac577eb2169c8) by blankwu).
- Modify the agent .env.example annotation ([359c6dc](https://github.com/citahub/cita-monitor/commit/359c6dcad118324cbd3ec84fe433199fead4ed8c) by JiangXL).

### Documented
- Docs: update readme about introduction ([e5d9f00](https://github.com/citahub/cita-monitor/commit/e5d9f0072850907cfe8e5d1a40c00064beced1ad) by RainChen).
- Docs: add coding style guide for prometheus ([44ea685](https://github.com/citahub/cita-monitor/commit/44ea68508037e3eb38bdc97514efb109c37c348c) by RainChen).
- Update agent readme ([57fa9a5](https://github.com/citahub/cita-monitor/commit/57fa9a5da3d8b16b6731fa63fa2b31d66215fac7) by JiangXL).
- Update grafana build command readme ([e98bd4b](https://github.com/citahub/cita-monitor/commit/e98bd4b16934c121df5421df980b4a474f9e7048) by blankwu).

### Fixed
- Fix show full pie chart, delete dup ip and port information ([9bc30b6](https://github.com/citahub/cita-monitor/commit/9bc30b659f6c7cf4708cb39e188672797c87c3ab) by blankwu).
- Fix the new version image and get the cita version number. ([0d8a763](https://github.com/citahub/cita-monitor/commit/0d8a7633c2d2f3d9a94bf1d243bd0b45eccaa7a5) by JiangXL).
- Fix dockerfile comment ([f0c8717](https://github.com/citahub/cita-monitor/commit/f0c87172b2fdd545650bbd5248285e6fde548db2) by blankwu).
- Fix container startup failed after modifying docker-compose.xml service name ([154729d](https://github.com/citahub/cita-monitor/commit/154729ddb2b5bc04215ce7c596806f75081f094a) by JiangXL).

### Removed
- Remove redundant readme ([3fc0234](https://github.com/citahub/cita-monitor/commit/3fc02346d2dd2a17cafe800e37c7fa9848c7cefa) by JiangXL).
- Remove timezone from docker-compose.xml ([da017ab](https://github.com/citahub/cita-monitor/commit/da017ab5cd73432218e46a6bcf8e302b50c4569a) by JiangXL).

### Misc
- Specify flask and psuti version number ([abbba92](https://github.com/citahub/cita-monitor/commit/abbba929b17803d984717982153d1355017977d3) by JiangXL).
- Reduce the size of the cita-exporter-image from 970mb to 478mb ([1b27e5d](https://github.com/citahub/cita-monitor/commit/1b27e5d8498662d7010083340f6adcbbf72e6a3e) by JiangXL).
- Allow to start test node using cita v0.24.0 ([7f07819](https://github.com/citahub/cita-monitor/commit/7f07819f4a17458c4afbedc7840234f5cd2f4b26) by RainChen).


## [v0.3.0](https://github.com/citahub/cita-monitor/releases/tag/v0.3.0) ([compare](https://github.com/citahub/cita-monitor/compare/v0.2.0...v0.3.0)) - 2019-06-05

### Added
- Add devtools/release/keepachangelog-template ([92dffa1](https://github.com/citahub/cita-monitor/commit/92dffa1baf0b2a5bfb6f2086f8f2bc310e0cfbf6) by RainChen).
- Add make receipts for release flow ([1ac3c44](https://github.com/citahub/cita-monitor/commit/1ac3c440033d16a956b5e469f61ec2c87db9b5c3) by RainChen).
- Add voter graph ([58b4ce2](https://github.com/citahub/cita-monitor/commit/58b4ce213f6a725a9b4c20a598ac9b385a0897ac) by blankwu).
- Add vote status ([9463eed](https://github.com/citahub/cita-monitor/commit/9463eed2db5c8ac368971cce02143e9120922162) by blankwu).
- Add `make changelog` to generate changelog.md from git logs ([64d823b](https://github.com/citahub/cita-monitor/commit/64d823b21669f68a739440926b9e8ed2e514fd58) by RainChen).
- Add used and free disk values ([078acf5](https://github.com/citahub/cita-monitor/commit/078acf56369061413f79ca64ed1b2063548db020) by blankwu).
- Add hard disk remaining space information ([ea660e4](https://github.com/citahub/cita-monitor/commit/ea660e40aaa32ecdeb91b2853c9a40ab1bc21ddf) by JiangXL).

### Documented
- Docs: add badges in readme ([4a77b43](https://github.com/citahub/cita-monitor/commit/4a77b43ff2e57d20f64d2c0b1ea27ce4a39384f5) by RainChen).
- Docs: update readme ([56a88c8](https://github.com/citahub/cita-monitor/commit/56a88c8cbbe976a91b1f38b6e2302b20c8000893) by RainChen).
- Docs: rename docs/alert_strategies.md to docs/alert_policies.md ([e07de43](https://github.com/citahub/cita-monitor/commit/e07de43d9129bd591428c3671302008139cc36fb) by RainChen).

### Fixed
- Fix vote list dup, add node id label query ([d1da247](https://github.com/citahub/cita-monitor/commit/d1da2479111e6c0f80cf6735660cdfebcf41eb40) by blankwu).
- Fix docker image name and docker container name ([8f11e3a](https://github.com/citahub/cita-monitor/commit/8f11e3ab88bb32162870cbd7b9c8f3d9c6ab856d) by blankwu).
- Fix python format, del node dir multipath ([9aeea21](https://github.com/citahub/cita-monitor/commit/9aeea21d69f424e85edbd306958faa5a9c42cf7b) by blankwu).
- Fix: make `make lint-shell-code` works in linux ([8532651](https://github.com/citahub/cita-monitor/commit/8532651a888fe69a131bf7a4214dafdbab546185) by RainChen).
- Fix: install requirements for agent/cita_exporter in `make deps` ([2427dd9](https://github.com/citahub/cita-monitor/commit/2427dd96735cd1689dfcd19ce18c773da6d74b03) by RainChen).

### Misc
- Bump version to v0.3.0 ([6390089](https://github.com/citahub/cita-monitor/commit/63900895a67cfeecbf2d2e2b45937c5e9dff3d21) by RainChen).
- Update the readme description of the agent and server ([9c024fb](https://github.com/citahub/cita-monitor/commit/9c024fbf1423263ca1a3118b4adb0b64873253b4) by JiangXL).
- Update script format ([05652bc](https://github.com/citahub/cita-monitor/commit/05652bc35a82390c8e337b6b986c97ab4250927a) by blankwu).
- Update the cita node info dashboard layout ([a1b9fbb](https://github.com/citahub/cita-monitor/commit/a1b9fbbdc766bead93b3097530d15df4660355c4) by JiangXL).
- Update dashboard, fix pie graph ([6c4cfd7](https://github.com/citahub/cita-monitor/commit/6c4cfd7123e9a984d3ff035987fe51e78b771445) by blankwu).
- Chore: disable some pylint modules for now ([d2c24a4](https://github.com/citahub/cita-monitor/commit/d2c24a496bdad8c707a79eb659ab332e4667ca68) by RainChen).
- Refactor: unnecessary "else" after "return" (no-else-return) ([c32484e](https://github.com/citahub/cita-monitor/commit/c32484e91a490d245a23280ee6912e90ac2a7b06) by RainChen).
- Refactor: trailing newlines (trailing-newlines) ([21046c6](https://github.com/citahub/cita-monitor/commit/21046c693ac28f904b0bffa94781f83807089262) by RainChen).
- Refactor: unnecessary parens after 'return' keyword (superfluous-parens) ([ce58526](https://github.com/citahub/cita-monitor/commit/ce58526445ea0549a9fcc95ff410a78cea710900) by RainChen).


## [v0.2.0](https://github.com/citahub/cita-monitor/releases/tag/v0.2.0) ([compare](https://github.com/citahub/cita-monitor/compare/v0.1.0...v0.2.0)) - 2019-05-16

### Added
- Add image tag, lock version, update dashboard ([76ac8ea](https://github.com/citahub/cita-monitor/commit/76ac8ea0f8cb9bdacd789bb27b2384dfeef8cb94) by blankwu).
- Add travisci config: .travis.yml ([98e342e](https://github.com/citahub/cita-monitor/commit/98e342e050e53a3a0f09f68f03e55c3d1230651a) by RainChen).
- Add dir map and change alertmanager subject name ([fb1c879](https://github.com/citahub/cita-monitor/commit/fb1c879fbdf2195686ae702ba633cdc73793c4e5) by blankwu).
- Add email template ([38273ef](https://github.com/citahub/cita-monitor/commit/38273ef92926e4cdb26b8ae12a722ae8c1c8b890) by blankwu).
- Add rule reame ([40548f5](https://github.com/citahub/cita-monitor/commit/40548f55265bf6ca020c02aafcf6490ab3e2f22f) by blankwu).
- Add new rules and format annotations ([24ea54b](https://github.com/citahub/cita-monitor/commit/24ea54bca8892c563f16f176834f3f24ca0d04d5) by blankwu).
- Add makefile ([3abdd13](https://github.com/citahub/cita-monitor/commit/3abdd132ac81ed51e558f3b736ef503f56dbba38) by RainChen).

### Changed
- Change index key is node id, add node rpc info and node id. ([695e7df](https://github.com/citahub/cita-monitor/commit/695e7df7a712c40bc90f2b0d7e677963bc4174ed) by blankwu).

### Documented
- Docs: fix typo for cita ([ab931f9](https://github.com/citahub/cita-monitor/commit/ab931f9f64bf8235941af545e16f8b40888634de) by RainChen).
- Docs: add readme-cn.md ([826561c](https://github.com/citahub/cita-monitor/commit/826561c02e01ec3cb3cb2cb24ad9f23150a94407) by RainChen).
- Docs: add system architecture，tech stack in readme ([e1caa84](https://github.com/citahub/cita-monitor/commit/e1caa84c3209e0b509769fbb4dcaeb6f08fec062) by RainChen).
- Docs: update readme and add alert_strategies.md, information_architecture.md to docs/ ([0280673](https://github.com/citahub/cita-monitor/commit/0280673290e0d7ccbf3d7cfb5ee1d4a64b372015) by RainChen).
- Docs: add screenshots in readme ([2cb2b23](https://github.com/citahub/cita-monitor/commit/2cb2b23dae3fef1ad22b401c3f55e1cf58e8b103) by RainChen).

### Fixed
- Fix prefix info ([11253a5](https://github.com/citahub/cita-monitor/commit/11253a5660ffe9ec5cc0eea4aaee2dec721e2b99) by wuxc).
- Fix cpu title ([e6d672a](https://github.com/citahub/cita-monitor/commit/e6d672a1567a23165de7369094aa457bfa3883c7) by wuxc).
- Fix docker start single container command description ([71bdefb](https://github.com/citahub/cita-monitor/commit/71bdefb70b94eb86197ee5cb44ca60af25143238) by blankwu).
- Fix container time sync, use file map ([a0bcbc9](https://github.com/citahub/cita-monitor/commit/a0bcbc9eb029f1f96a28b8335df212c158bf7135) by blankwu).
- Fix: request command causes the script to fail to run ([b14d5a6](https://github.com/citahub/cita-monitor/commit/b14d5a644b940a0bad805b4fdf8ec7c1008ca579) by blankwu).
- Fix 4 consensus nodes to get 5 bug ([17b76d4](https://github.com/citahub/cita-monitor/commit/17b76d40a592e88db3e1a2fadb0295a790538cc0) by JiangXL).

### Misc
- Polish readme ([98bdde4](https://github.com/citahub/cita-monitor/commit/98bdde4ada6622c71f33be515b2371d527c06107) by zhouyun-zoe).
- Del interval select ([883f773](https://github.com/citahub/cita-monitor/commit/883f773f6f73ddc9d5f461a77d73d946dc747ef5) by blankwu).
- Modify the variables of the docker-compose configuration file to uppercase ([a0bd212](https://github.com/citahub/cita-monitor/commit/a0bd212627686f0b2d1c851468c5d8d935f53d2a) by JiangXL).
- Optimized the code format and improved the qa score to 9.63 (your code has been rated at 9.63/10) ([1ec0474](https://github.com/citahub/cita-monitor/commit/1ec0474ecf934122a417eb364c82f68168349b61) by JiangXL).
- Format code, update variable name ([3f69cd4](https://github.com/citahub/cita-monitor/commit/3f69cd4f0f108a29ed55e077091faf86d2a9be3c) by blankwu).
-   update server readme ([02f2917](https://github.com/citahub/cita-monitor/commit/02f291744d51c19ec1a22be4aebfd6e012171692) by JiangXL).
- Set the default alarm mailbox configuration ([5d92cee](https://github.com/citahub/cita-monitor/commit/5d92ceedb5b22c8735f2e2da3beac3b6d942108d) by JiangXL).
- Recover cita node info dashboard id ([04eb5e8](https://github.com/citahub/cita-monitor/commit/04eb5e85c372be0435402fe795931dc1515f45b6) by blankwu).
-   fix the 0.19.1 version of cita does not exist. the quotaused program cannot run. ([9127536](https://github.com/citahub/cita-monitor/commit/9127536b33b536c389e0cb86fd9426b654758b70) by JiangXL).
- Recover config, del rabbitmq info ([95ee4d3](https://github.com/citahub/cita-monitor/commit/95ee4d36e6f99892bf0d0454612af9b70eab7df1) by blankwu).
- Update agent readme ([66caa90](https://github.com/citahub/cita-monitor/commit/66caa908a5ca23a6df53a4f2743a29b7b09e3322) by JiangXL).
- Homemade grafana image, reducing grafana startup time ([6e579db](https://github.com/citahub/cita-monitor/commit/6e579db8b4a045301e6b7b47a816613fcd1f1e32) by JiangXL).
- Refactor: format agent/cita_monitor_agent.py with formatter config ([a2430d5](https://github.com/citahub/cita-monitor/commit/a2430d5e5d1cbed047aee51a649f84b31fe3a319) by RainChen).
- Update makefile to add receipts: lint-python-code format-python-code lint-shell-code format-shell-code ([d590cd0](https://github.com/citahub/cita-monitor/commit/d590cd098540dc1608980bee9e6380d2c53897a4) by RainChen).
- Delete the ci_install.sh script ([96102f9](https://github.com/citahub/cita-monitor/commit/96102f9eb9a6cbacc5e28868af7fe6d0a99b8521) by JiangXL).
- Modify the directory name cita-monitor-agent for agent, cita-monitor-server for server ([7440257](https://github.com/citahub/cita-monitor/commit/7440257b8d6122deb3770e575e0b77c0c37e4e60) by JiangXL).
- Reduce the number of custom parameters ([82d88dc](https://github.com/citahub/cita-monitor/commit/82d88dc7913aabfac064826eac717e16886da6f6) by JiangXL).
- Create license ([1560354](https://github.com/citahub/cita-monitor/commit/1560354a0077eba24c7d28bd1d706310b1db6c6e) by Rain Chen).


## [v0.1.0](https://github.com/citahub/cita-monitor/releases/tag/v0.1.0) ([compare](https://github.com/citahub/cita-monitor/compare/84b2f96431eeb275185a4c8fb9fe3a52bedededf...v0.1.0)) - 2019-04-29

### Added
- Add rabbitmq-server collect, change collection method ([cad674a](https://github.com/citahub/cita-monitor/commit/cad674acdbd91305a17d19d2b4c7c1cf9b37a984) by blankwu).
- Add readme for getting started and contributing ([e6e4e3e](https://github.com/citahub/cita-monitor/commit/e6e4e3ef7bb2a5af7e4d0eb5e2f0badee89b1ac3) by RainChen).
- Add alert, and update alertmanager name ([5c6f731](https://github.com/citahub/cita-monitor/commit/5c6f73105258bb94caea9035cee27338cd17b7cf) by blankwu).
- Add quota info and change label name ([a445930](https://github.com/citahub/cita-monitor/commit/a445930627c9ef41ae58142b83ced84b28d8816d) by blankwu).
- Add quota info ([2dc4f01](https://github.com/citahub/cita-monitor/commit/2dc4f017c7e4f682fb28a0b4d13b45d4ce7bfb42) by blankwu).
- Add ci host auto deployment script; ([0faef05](https://github.com/citahub/cita-monitor/commit/0faef0504f0c490460a2927fcb1dd7d5c93f5cad) by blankwu).

### Changed
- Change point size, border alignment ([33c2c54](https://github.com/citahub/cita-monitor/commit/33c2c54dca430d5060102ff3099451c809220a17) by blankwu).
- Change volume path; add 'check_env_port' string; ([02cee93](https://github.com/citahub/cita-monitor/commit/02cee93719a878ec696d8425b4914e383d5cf263) by blankwu).

### Documented
- Docs: add coding style for shell ([ddfd884](https://github.com/citahub/cita-monitor/commit/ddfd8847c6a98997ed8eb83b33fb4837ed81bede) by RainChen).

### Fixed
- Fix grafana redeploy admin password is reset ([af56b34](https://github.com/citahub/cita-monitor/commit/af56b34d9b267ab3a66867f95a48d556bce9f00c) by JiangXL).
- Fix old version cita no address file script crash problem ([51d5c4d](https://github.com/citahub/cita-monitor/commit/51d5c4d628e339b28c34ec3767df37be30192c1f) by jiangxianliang).

### Misc
- Update readme ([a3c5ca6](https://github.com/citahub/cita-monitor/commit/a3c5ca6d0b8d6694a8f3a6d57f489f05e5e9f82b) by blankwu).
- Refactor: format ci_install.sh with shfmt ([a82f51a](https://github.com/citahub/cita-monitor/commit/a82f51a32c47c51a0e06188f1b2202bd0ebd5d50) by RainChen).
- Refactor: format shell code with code formatterr ([a8aa5b6](https://github.com/citahub/cita-monitor/commit/a8aa5b61f4d7199932181f6c51c9e12948b9af84) by RainChen).
- Refactor: format cita_monitor_agent.py with formatter yapf ([b9f8190](https://github.com/citahub/cita-monitor/commit/b9f8190a55157e1d33d9de3e1402271b0fbbd2f3) by RainChen).
- Format python script ([c7f3e8f](https://github.com/citahub/cita-monitor/commit/c7f3e8fa2371d07fd8dde482b4f619e4cfa97f42) by blankwu).
- Update variable name ([8a7b4ca](https://github.com/citahub/cita-monitor/commit/8a7b4cac62f03d6656fef0797f9ea1d338effc2c) by blankwu).
- Update labels name ([2d1e9c6](https://github.com/citahub/cita-monitor/commit/2d1e9c68e437a643809119ae09139a9cf6910226) by blankwu).
- Format script and add comment ([7088d6f](https://github.com/citahub/cita-monitor/commit/7088d6f04599a293c7ba8bb42709e348ce13adeb) by blankwu).
- Set default grfana login password to 'admin' ([c898fae](https://github.com/citahub/cita-monitor/commit/c898faef7468966a45ae3ec623fdaf90748a62fe) by blankwu).
- Sync prometheus job name; ([0342010](https://github.com/citahub/cita-monitor/commit/03420101bf13d3bf429dfe5b5287c820f0a8c2f1) by blankwu).
- Modify cita_monitor_agent.py in ci scripts to mount as an absolute path ([18efc5b](https://github.com/citahub/cita-monitor/commit/18efc5b46770d9fa6e2f48dff66c9a0b67c12068) by jiangxianliang).
- Modify yml file indentation ([a27ced7](https://github.com/citahub/cita-monitor/commit/a27ced7848a127a3bc18d46d8aafe8070faf6274) by jiangxianliang).
- Specification directory structure, name changed to lowercase ([5344bf5](https://github.com/citahub/cita-monitor/commit/5344bf567bab117900f15cbaef47fd3c181c38b3) by jiangxianliang).
- Citanodeinfodashboard modify indicator unit; ([397a4da](https://github.com/citahub/cita-monitor/commit/397a4da8402da2b781eec62c71f6d370b73eaf47) by blankwu).
- New dashboard; new script; ([d7fdc4e](https://github.com/citahub/cita-monitor/commit/d7fdc4e4b77e6732bd2a4afcb16435c1da06a78f) by blankwu).
- Update ci_install.sh, default running other node monitor; ([8e031dd](https://github.com/citahub/cita-monitor/commit/8e031dd729df745d2f39b4b0d627eb11df696d4f) by blankwu).
- Server: update default node ip info; ([37ccf56](https://github.com/citahub/cita-monitor/commit/37ccf56bfcf79a6db87340953a03afd466d568a7) by blankwu).
- Agent: update default node dir; ([c3b1757](https://github.com/citahub/cita-monitor/commit/c3b175780caaa727c80fed418acae31c12c8f462) by blankwu).
- Server: update citaagentexporterdashboard, support automatically switch node id; ([eb07e49](https://github.com/citahub/cita-monitor/commit/eb07e49d068c5cc30cb4362b968afda28fb7d15c) by blankwu).
- Server: change 'node' to 'host'; ([703c4d6](https://github.com/citahub/cita-monitor/commit/703c4d69ef42dce911ff1db965c722a0956cb792) by blankwu).
- Update directory architecture ([e7b8429](https://github.com/citahub/cita-monitor/commit/e7b84292bb50b1e15f613606818c9e7d02662259) by blankwu).
- Adjust the agent directory structure ([02341dd](https://github.com/citahub/cita-monitor/commit/02341ddf17303c919c914647846068a0fd72b5e1) by jiangxianliang).
- Modify the docker-compose.yml and dockerfile format normalization ([7ebc3db](https://github.com/citahub/cita-monitor/commit/7ebc3db75747855b54a75adf7997554fdc647b7f) by jiangxianliang).
- Agent: del error variable from process_list.yml; update readme; ([097f0cf](https://github.com/citahub/cita-monitor/commit/097f0cf9757dfefa697d3580e218a94ddce2c3f4) by blankwu).
- Server: add env file; change server compose.yml use env file and new hostname; ([ed2e5de](https://github.com/citahub/cita-monitor/commit/ed2e5de64cf9147bcf095d0580edc02eb7a545bd) by blankwu).
- Agent: add agent image build files; ([d69cf61](https://github.com/citahub/cita-monitor/commit/d69cf61efbd363eca858365c01bc1ac513689c8b) by blankwu).
- Agent: add agent files; change directory name; ([6e0626e](https://github.com/citahub/cita-monitor/commit/6e0626eb21e78811370d034781704a720d6bde17) by blankwu).
- Server: del old files; update dashboard files; ([26fcf5a](https://github.com/citahub/cita-monitor/commit/26fcf5ad52759c47500917625d7b1d50b733701f) by blankwu).
- Create some ddir ([f8d0048](https://github.com/citahub/cita-monitor/commit/f8d0048594c6d6504a432601f1d3e530d5878128) by blankwu).
- Create docker-compose_build directory ([abb77af](https://github.com/citahub/cita-monitor/commit/abb77af6038a741815e38881ca546b4235a5f4ea) by blankwu).
- Delete old files ([46e2cb9](https://github.com/citahub/cita-monitor/commit/46e2cb974184fd0a5ccf360470e9bf5a460cce21) by blankwu).
- Create dockerfile build cita_agent clien ([5e8632f](https://github.com/citahub/cita-monitor/commit/5e8632f18521f1083a37d01e281125d7df397c21) by blankwu).
- Init project ([84b2f96](https://github.com/citahub/cita-monitor/commit/84b2f96431eeb275185a4c8fb9fe3a52bedededf) by RainChen).


