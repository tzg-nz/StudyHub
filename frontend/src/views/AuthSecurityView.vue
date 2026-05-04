<template>
  <div style="max-width: 1100px; margin: 0 auto;">
    <a-page-header title="认证安全对比" sub-title="体验不同攻击方式对三种认证的影响" @back="$router.push('/')" />

    <a-alert
      message="本页面仅用于学习目的，演示常见Web安全漏洞对不同认证方式的影响"
      type="warning"
      show-icon
      style="margin-bottom: 24px;"
    />

    <a-tabs v-model:activeKey="activeTab" type="card">
      <a-tab-pane key="overview" tab="📊 优劣对比">
        <a-row :gutter="16" style="margin-bottom: 24px;">
          <a-col :span="8">
            <a-card size="small" title="🔐 Session认证" :bordered="false" style="background: #e6f7ff;">
              <p><strong>存储位置：</strong>服务端（数据库/缓存）</p>
              <p><strong>传输方式：</strong>Cookie（sessionid）</p>
              <p><strong>状态：</strong>有状态</p>
              <a-divider style="margin: 8px 0;" />
              <p style="color: #52c41a;"><strong>✅ 优势</strong></p>
              <ul style="padding-left: 16px; font-size: 13px;">
                <li>服务端可随时撤销会话</li>
                <li>Session ID 无意义，无法被伪造</li>
                <li>服务端完全控制会话生命周期</li>
                <li>适合需要即时踢人的场景</li>
              </ul>
              <p style="color: #ff4d4f;"><strong>❌ 劣势</strong></p>
              <ul style="padding-left: 16px; font-size: 13px;">
                <li>服务端需存储Session，扩展性差</li>
                <li>分布式部署需共享Session</li>
                <li>需配合CSRF Token或SameSite防护</li>
                <li>跨域场景处理复杂</li>
              </ul>
              <a-divider style="margin: 8px 0;" />
              <p><strong>🎯 适用场景</strong></p>
              <ul style="padding-left: 16px; font-size: 13px;">
                <li>传统服务端渲染应用</li>
                <li>需要即时会话管理的系统</li>
                <li>同域名下的Web应用</li>
              </ul>
            </a-card>
          </a-col>
          <a-col :span="8">
            <a-card size="small" title="🔑 Token(JWT)认证" :bordered="false" style="background: #f6ffed;">
              <p><strong>存储位置：</strong>客户端（localStorage）</p>
              <p><strong>传输方式：</strong>Authorization 请求头</p>
              <p><strong>状态：</strong>无状态</p>
              <a-divider style="margin: 8px 0;" />
              <p style="color: #52c41a;"><strong>✅ 优势</strong></p>
              <ul style="padding-left: 16px; font-size: 13px;">
                <li>无状态，服务端不存储</li>
                <li>天然支持分布式/微服务</li>
                <li>跨域友好（CORS）</li>
                <li>不受CSRF攻击影响</li>
                <li>移动端友好</li>
              </ul>
              <p style="color: #ff4d4f;"><strong>❌ 劣势</strong></p>
              <ul style="padding-left: 16px; font-size: 13px;">
                <li>Token签发后无法主动撤销</li>
                <li>Token体积较大（含用户信息）</li>
                <li>存在XSS攻击风险</li>
                <li>Token续期方案复杂</li>
              </ul>
              <a-divider style="margin: 8px 0;" />
              <p><strong>🎯 适用场景</strong></p>
              <ul style="padding-left: 16px; font-size: 13px;">
                <li>前后端分离项目</li>
                <li>移动端App / 小程序</li>
                <li>微服务架构</li>
                <li>第三方API对接</li>
              </ul>
            </a-card>
          </a-col>
          <a-col :span="8">
            <a-card size="small" title="🍪 Cookie认证" :bordered="false" style="background: #fff7e6;">
              <p><strong>存储位置：</strong>浏览器Cookie</p>
              <p><strong>传输方式：</strong>Cookie自动携带</p>
              <p><strong>状态：</strong>无状态（JWT在Cookie中）</p>
              <a-divider style="margin: 8px 0;" />
              <p style="color: #52c41a;"><strong>✅ 优势</strong></p>
              <ul style="padding-left: 16px; font-size: 13px;">
                <li>HttpOnly 防止XSS窃取</li>
                <li>SameSite 防止CSRF</li>
                <li>浏览器自动管理生命周期</li>
                <li>兼具JWT无状态和Cookie安全性</li>
              </ul>
              <p style="color: #ff4d4f;"><strong>❌ 劣势</strong></p>
              <ul style="padding-left: 16px; font-size: 13px;">
                <li>Cookie有4KB大小限制</li>
                <li>跨域配置复杂</li>
                <li>仍存在CSRF风险（配置不当时）</li>
                <li>子域名Cookie共享需谨慎</li>
              </ul>
              <a-divider style="margin: 8px 0;" />
              <p><strong>🎯 适用场景</strong></p>
              <ul style="padding-left: 16px; font-size: 13px;">
                <li>同域前后端分离项目</li>
                <li>需要兼顾安全和便捷的场景</li>
                <li>对XSS防护要求高的系统</li>
              </ul>
            </a-card>
          </a-col>
        </a-row>

        <a-card title="📋 特性对比表" :bordered="false">
          <a-table :dataSource="compareTable" :columns="compareColumns" :pagination="false" size="small" bordered />
        </a-card>
      </a-tab-pane>

      <a-tab-pane key="xss" tab="🐛 XSS攻击">
        <a-card title="XSS（跨站脚本攻击）" :bordered="false">
          <a-alert
            message="XSS攻击原理：攻击者注入恶意JavaScript代码，可窃取凭证、冒充用户发请求、窃取页面内容、监听用户输入"
            type="info"
            show-icon
            style="margin-bottom: 16px;"
          />
          <a-row :gutter="16" style="margin-bottom: 16px;">
            <a-col :span="8">
              <a-card size="small" title="Session vs XSS" :bordered="false" style="background: #e6f7ff; min-height: 160px; display: flex; flex-direction: column;">
                <a-tag color="orange" style="margin-bottom: 8px;">部分防护</a-tag>
                <p style="font-size: 13px; flex: 1;">HttpOnly 防止 JS 读取 sessionid，但攻击者仍可通过 XSS 读取 csrftoken 并直接发请求冒充用户</p>
                <a-button type="primary" danger size="small" @click="$router.push('/attack-process?type=xss&auth=session')" style="margin-top: auto;">
                  🎬 演示
                </a-button>
              </a-card>
            </a-col>
            <a-col :span="8">
              <a-card size="small" title="Token vs XSS" :bordered="false" style="background: #f6ffed; min-height: 160px; display: flex; flex-direction: column;">
                <a-tag color="red" style="margin-bottom: 8px;">⚠️ 高危</a-tag>
                <p style="font-size: 13px; flex: 1;">localStorage 中的 Token 可被 JS 直接读取，攻击者可轻松窃取</p>
                <a-button type="primary" danger size="small" @click="$router.push('/attack-process?type=xss&auth=token')" style="margin-top: auto;">
                  🎬 演示
                </a-button>
              </a-card>
            </a-col>
            <a-col :span="8">
              <a-card size="small" title="Cookie vs XSS" :bordered="false" style="background: #fff7e6; min-height: 160px; display: flex; flex-direction: column;">
                <a-tag color="orange" style="margin-bottom: 8px;">🟡 部分防护</a-tag>
                <p style="font-size: 13px; flex: 1;">HttpOnly 阻止 Token 被窃取，但 XSS 仍可在页面内发请求、窃取数据</p>
                <a-button type="primary" danger size="small" @click="$router.push('/attack-process?type=xss&auth=cookie')" style="margin-top: auto;">
                  🎬 演示
                </a-button>
              </a-card>
            </a-col>
          </a-row>
        </a-card>
      </a-tab-pane>

      <a-tab-pane key="csrf" tab="🛡️ CSRF攻击">
        <a-card title="CSRF（跨站请求伪造）" :bordered="false">
          <a-alert
            message="CSRF攻击原理：攻击者诱导用户访问恶意网站，利用浏览器自动携带Cookie的特性，冒充用户发起请求"
            type="info"
            show-icon
            style="margin-bottom: 16px;"
          />
          <a-row :gutter="16" style="margin-bottom: 16px;">
            <a-col :span="8">
              <a-card size="small" title="Session vs CSRF" :bordered="false" style="background: #e6f7ff; min-height: 160px; display: flex; flex-direction: column;">
                <a-tag color="orange" style="margin-bottom: 8px;">部分防护</a-tag>
                <p style="font-size: 13px; flex: 1;">SameSite=Lax 阻止跨站携带 Cookie，简单跨站请求会被阻止，但复杂场景仍有风险</p>
                <a-button type="primary" danger size="small" @click="$router.push('/attack-process?type=csrf&auth=session')" style="margin-top: auto;">
                  🎬 演示
                </a-button>
              </a-card>
            </a-col>
            <a-col :span="8">
              <a-card size="small" title="Token vs CSRF" :bordered="false" style="background: #f6ffed; min-height: 160px; display: flex; flex-direction: column;">
                <a-tag color="green" style="margin-bottom: 8px;">✅ 安全</a-tag>
                <p style="font-size: 13px; flex: 1;">Authorization 头不会被浏览器自动携带，天然免疫 CSRF</p>
                <a-button type="primary" danger size="small" @click="$router.push('/attack-process?type=csrf&auth=token')" style="margin-top: auto;">
                  🎬 演示
                </a-button>
              </a-card>
            </a-col>
            <a-col :span="8">
              <a-card size="small" title="Cookie vs CSRF" :bordered="false" style="background: #fff7e6; min-height: 160px; display: flex; flex-direction: column;">
                <a-tag color="orange" style="margin-bottom: 8px;">部分防护</a-tag>
                <p style="font-size: 13px; flex: 1;">SameSite=Lax 阻止跨站携带 Cookie，配置与 Session 完全一致</p>
                <a-button type="primary" danger size="small" @click="$router.push('/attack-process?type=csrf&auth=cookie')" style="margin-top: auto;">
                  🎬 演示
                </a-button>
              </a-card>
            </a-col>
          </a-row>
        </a-card>
      </a-tab-pane>

      <a-tab-pane key="token-theft" tab="🔑 Token窃取">
        <a-card title="凭证泄露与滥用" :bordered="false">
          <a-alert
            message="演示如果认证凭证被窃取后，三种认证方式的不同影响和恢复手段"
            type="info"
            show-icon
            style="margin-bottom: 16px;"
          />
          <a-row :gutter="16" style="margin-bottom: 16px;">
            <a-col :span="8">
              <a-card size="small" title="🔐 Session泄露" :bordered="false" style="background: #e6f7ff; min-height: 160px; display: flex; flex-direction: column;">
                <a-tag color="green" style="margin-bottom: 8px;">✅ 可即时撤销</a-tag>
                <p style="font-size: 13px; flex: 1;">服务端销毁 Session，攻击者手中的 sessionid 和 csrftoken 立即失效</p>
                <a-button type="primary" danger size="small" @click="$router.push('/attack-process?type=theft&auth=session')" style="margin-top: auto;">
                  🎬 演示
                </a-button>
              </a-card>
            </a-col>
            <a-col :span="8">
              <a-card size="small" title="🔑 Token泄露" :bordered="false" style="background: #f6ffed; min-height: 160px; display: flex; flex-direction: column;">
                <a-tag color="red" style="margin-bottom: 8px;">⚠️ 无法撤销</a-tag>
                <p style="font-size: 13px; flex: 1;">JWT 签发后无法主动撤销，只能等待自然过期</p>
                <a-button type="primary" danger size="small" @click="$router.push('/attack-process?type=theft&auth=token')" style="margin-top: auto;">
                  🎬 演示
                </a-button>
              </a-card>
            </a-col>
            <a-col :span="8">
              <a-card size="small" title="🍪 Cookie泄露" :bordered="false" style="background: #fff7e6; min-height: 160px; display: flex; flex-direction: column;">
                <a-tag color="orange" style="margin-bottom: 8px;">部分可控</a-tag>
                <p style="font-size: 13px; flex: 1;">无法撤销 Token，但可缩短有效期减少风险窗口</p>
                <a-button type="primary" danger size="small" @click="$router.push('/attack-process?type=theft&auth=cookie')" style="margin-top: auto;">
                  🎬 演示
                </a-button>
              </a-card>
            </a-col>
          </a-row>
        </a-card>
      </a-tab-pane>

      <a-tab-pane key="summary" tab="📝 安全总结">
        <a-card title="三种认证方式安全总结" :bordered="false">
          <a-table :dataSource="securityTable" :columns="securityColumns" :pagination="false" size="small" bordered />

          <a-divider>最佳实践建议</a-divider>

          <a-row :gutter="16">
            <a-col :span="12">
              <a-card size="small" title="🛡️ Session认证安全建议" :bordered="false">
                <ul style="padding-left: 16px; font-size: 13px;">
                  <li>设置 Cookie <code>HttpOnly</code> + <code>SameSite=Lax</code></li>
                  <li>或使用 CSRF Token 双重验证（更严格）</li>
                  <li>Session ID 使用足够长的随机值</li>
                  <li>登录后重新生成 Session ID</li>
                  <li>设置合理的 Session 过期时间</li>
                </ul>
              </a-card>
            </a-col>
            <a-col :span="12">
              <a-card size="small" title="🛡️ Token(JWT)安全建议" :bordered="false">
                <ul style="padding-left: 16px; font-size: 13px;">
                  <li>设置较短的 Access Token 过期时间（15-60分钟）</li>
                  <li>使用 Refresh Token 续期机制</li>
                  <li>实现 Token 黑名单（虽违背无状态原则）</li>
                  <li>严格防止XSS漏洞（输入过滤 + CSP）</li>
                  <li>不在 Token 中存储敏感信息</li>
                </ul>
              </a-card>
            </a-col>
          </a-row>
          <a-row :gutter="16" style="margin-top: 16px;">
            <a-col :span="12">
              <a-card size="small" title="🛡️ Cookie认证安全建议" :bordered="false">
                <ul style="padding-left: 16px; font-size: 13px;">
                  <li>必须设置 <code>HttpOnly</code> 防止XSS窃取</li>
                  <li>必须设置 <code>SameSite</code> 防止CSRF</li>
                  <li>设置 <code>Secure</code>（生产环境）仅HTTPS传输</li>
                  <li>设置较短的 Cookie 过期时间</li>
                  <li>使用 <code>Path</code> 限制Cookie作用范围</li>
                </ul>
              </a-card>
            </a-col>
            <a-col :span="12">
              <a-card size="small" title="🏆 综合推荐" :bordered="false" style="background: #f6ffed;">
                <a-typography-paragraph>
                  <strong>前后端分离项目（推荐）：</strong><br />
                  Cookie认证（HttpOnly + SameSite）+ 短期JWT<br />
                  兼顾安全性和无状态优势
                </a-typography-paragraph>
                <a-typography-paragraph>
                  <strong>传统服务端渲染：</strong><br />
                  Session认证 + CSRF Token<br />
                  最成熟的方案
                </a-typography-paragraph>
                <a-typography-paragraph>
                  <strong>移动端/第三方API：</strong><br />
                  Token(JWT)认证<br />
                  唯一可行的方案
                </a-typography-paragraph>
              </a-card>
            </a-col>
          </a-row>
        </a-card>
      </a-tab-pane>
    </a-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const activeTab = ref('overview')

const compareColumns = [
  { title: '特性', dataIndex: 'feature', key: 'feature', width: 150 },
  { title: '🔐 Session', dataIndex: 'session', key: 'session' },
  { title: '🔑 Token(JWT)', dataIndex: 'token', key: 'token' },
  { title: '🍪 Cookie', dataIndex: 'cookie', key: 'cookie' },
]

const compareTable = [
  { key: '1', feature: '存储位置', session: '服务端', token: '客户端(localStorage)', cookie: '浏览器Cookie' },
  { key: '2', feature: '传输方式', session: 'Cookie自动携带', token: 'Authorization头', cookie: 'Cookie自动携带' },
  { key: '3', feature: '状态', session: '有状态', token: '无状态', cookie: '无状态' },
  { key: '4', feature: '可撤销性', session: '✅ 即时撤销', token: '❌ 无法主动撤销', cookie: '❌ 无法主动撤销' },
  { key: '5', feature: 'XSS防护', session: '✅ HttpOnly防读取', token: '❌ JS可直接读取', cookie: '✅ HttpOnly防读取' },
  { key: '6', feature: 'CSRF防护', session: '🟡 SameSite部分防护', token: '✅ 天然免疫', cookie: '🟡 SameSite部分防护' },
  { key: '7', feature: '跨域支持', session: '❌ 困难', token: '✅ 友好', cookie: '🟡 需配置' },
  { key: '8', feature: '分布式支持', session: '❌ 需共享Session', token: '✅ 天然支持', cookie: '✅ 天然支持' },
  { key: '9', feature: '移动端支持', session: '❌ 不适合', token: '✅ 友好', cookie: '🟡 部分支持' },
  { key: '10', feature: '凭证大小', session: '小(SessionID)', token: '大(含用户信息)', cookie: '大(含用户信息)' },
  { key: '11', feature: '续期方式', session: '自动续期', token: 'Refresh Token', cookie: '重新设置Cookie' },
]

const securityColumns = [
  { title: '攻击类型', dataIndex: 'attack', key: 'attack', width: 120 },
  { title: '🔐 Session', dataIndex: 'session', key: 'session' },
  { title: '🔑 Token(JWT)', dataIndex: 'token', key: 'token' },
  { title: '🍪 Cookie', dataIndex: 'cookie', key: 'cookie' },
]

const securityTable = [
  { key: '1', attack: 'XSS窃取', session: '🟡 无法读取Cookie\n但可冒充发请求', token: '🔴 可直接读取\nlocalStorage', cookie: '🟡 无法读取Token\n但可页面内攻击' },
  { key: '2', attack: 'CSRF伪造', session: '🟡 SameSite\n部分防护', token: '🟢 不自动携带\nAuthorization头', cookie: '🟡 SameSite\n部分防护' },
  { key: '3', attack: '凭证泄露后', session: '🟢 可即时撤销\nSession', token: '🔴 无法撤销\n只能等过期', cookie: '🟡 无法撤销\n但可缩短有效期' },
  { key: '4', attack: '中间人攻击', session: '🟡 Secure标志\n仅HTTPS', token: '🔴 明文传输\n需HTTPS', cookie: '🟡 Secure标志\n仅HTTPS' },
]
</script>
