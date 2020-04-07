shellgei_discord
====

[シェル芸bot](https://github.com/theoremoon/ShellgeiBot)をDiscordでも．

## Description
Twitterで有名な[theoremoon](https://github.com/theoremoon)さんの[シェル芸bot](https://github.com/theoremoon/ShellgeiBot)をDiscord上で実現するbotです．

......といっても自力でDockerコンテナを動かしているわけではなく[jiro4989](https://github.com/jiro4989)さんの[websh](https://github.com/jiro4989/websh)のAPIを叩くだけ．


## Usage
- このbotへのメンションに反応してシェルコマンドを実行します．またその際このbotへのメンションはコードから削除されます．
- メンションなどのMessageFormatの文字数によるズレをなるべく吸収し，表示に近い字幅でシェルを実行します．
- コードブロック (\`\`\` ~ \`\`\`) が存在する場合，１つ目のコードブロックの中身のみをコードとして認識します．
- 30秒以上の処理はタイムアウトします．
- その他の仕様は本家のリポジトリか[こちら](https://furutsuki.hatenablog.com/entry/2018/07/13/221806)を御覧ください．


## Link
- [シェル芸bot (theoremoon)](https://github.com/theoremoon/ShellgeiBot): 本家大本
- [websh (jiro4989)](https://github.com/jiro4989/websh): API利用先
- [今の所判明しているシェル芸botの仕様](https://furutsuki.hatenablog.com/entry/2018/07/13/221806): Twitterのシェル芸botの仕様


## Licence

[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author

[kairi003](https://github.com/kairi003)