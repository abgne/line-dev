# LIFF Plugins & Extensions

## 1. LIFF Plugins

LIFF plugins extend the LIFF SDK with custom APIs or modify existing behavior. Available in LIFF SDK v2.19.0+.

### Plugin Interface

A plugin is an object or class with:
- `name` (string) — identifier, accessed as `liff.$[name]`
- `install(context, option)` — returns an object with methods/properties

```javascript
class GreetPlugin {
  constructor() {
    this.name = 'greet';
  }
  install(context, option) {
    return {
      hello: () => console.log('Hello!'),
      goodbye: () => console.log('Goodbye!'),
    };
  }
}

// Register
liff.use(new GreetPlugin());

// Use
liff.$greet.hello();    // "Hello!"
liff.$greet.goodbye();  // "Goodbye!"
```

### install() Context

```javascript
install(context, option) {
  // context.liff  — the liff object
  // context.hooks — hook registration methods
  // option        — custom config passed via liff.use(plugin, option)
}
```

### Object-based Plugin (alternative)

```javascript
const greetPlugin = {
  name: 'greet',
  install() {
    return {
      hello: () => console.log('Hello!'),
    };
  },
};
liff.use(greetPlugin);
```

### Single-function Plugin

If a plugin has only one API, `install()` can return a function directly instead of an object:

```javascript
class GreetPlugin {
  constructor() { this.name = 'greet'; }
  install() {
    return () => console.log('Hello!');
  }
}
liff.use(new GreetPlugin());
liff.$greet(); // "Hello!" — called directly, not liff.$greet.something()
```

### Activation Order

`liff.use()` must be called **before** `liff.init()` — execution after init is not guaranteed to work. This applies to both LIFF plugins and pluggable SDK modules.

---

## 2. Plugin Hooks

Plugins can register callbacks on LIFF lifecycle events.

### liff.init() Hooks

| Hook | Timing | Type |
|------|--------|------|
| `context.hooks.init.before` | Immediately after `liff.init()` called | Async |
| `context.hooks.init.after` | Before `successCallback` resolves | Async |

```javascript
class MyPlugin {
  name = 'my-plugin';
  install({ hooks }) {
    hooks.init.before(async () => {
      console.log('Before init');
    });
    hooks.init.after(async () => {
      console.log('After init');
    });
    return {};
  }
}
```

### Custom Hooks

Create plugin-specific hooks using `@liff/hooks`:

```javascript
import { SyncHook, AsyncHook } from '@liff/hooks';

class AnalyticsPlugin {
  constructor() {
    this.name = 'analytics';
    this.hooks = {
      beforeTrack: new SyncHook(),   // sequential, return values ignored
      afterTrack: new AsyncHook(),   // parallel via Promise.all()
    };
  }
  install() {
    return {
      track: (event) => {
        this.hooks.beforeTrack.call();
        // ... tracking logic ...
        this.hooks.afterTrack.call();
      },
    };
  }
}
```

| Hook Type | Execution | Callbacks |
|-----------|-----------|-----------|
| `SyncHook` | Sequential | Return values ignored |
| `AsyncHook` | Parallel (`Promise.all`) | Must return Promises |

### Passing Arguments via `call()`

`call()` accepts any number of arguments, which are forwarded to registered callbacks:

```javascript
// In your plugin:
this.hooks.beforeTrack.call('pageview', { url: '/home' });

// In another plugin's callback:
context.hooks.$analytics.beforeTrack((eventName, data) => {
  console.log(eventName, data); // 'pageview', { url: '/home' }
});
```

### Cross-plugin Hook Registration

Plugins can hook into **other plugins'** custom hooks via `context.hooks.$[pluginName]`:

```javascript
class LoggerPlugin {
  constructor() { this.name = 'logger'; }
  install(context) {
    // Hook into AnalyticsPlugin's custom hooks
    context.hooks.$analytics.beforeTrack(() => {
      console.log('Analytics tracking started');
    });
    context.hooks.$analytics.afterTrack(() => {
      console.log('Analytics tracking done');
      return Promise.resolve();
    });
  }
}

// Registration order matters: the plugin providing hooks must be registered first
liff.use(new AnalyticsPlugin());
liff.use(new LoggerPlugin());
```

---

## 3. Official Plugins

### LIFF Inspector
Debug LIFF apps using Chrome DevTools across devices.

- **npm**: `@line/liff-inspector`
- **GitHub**: [line/liff-inspector](https://github.com/line/liff-inspector)

```javascript
import liff from '@line/liff';
import LiffInspector from '@line/liff-inspector';

liff.use(new LiffInspector());
liff.init({ liffId: '...' });
```

### LIFF Mock
Test LIFF apps independently from LINE servers. Provides mock mode for local development.

- **npm**: `@line/liff-mock`
- **GitHub**: [line/liff-mock](https://github.com/line/liff-mock)

```javascript
import liff from '@line/liff';
import LiffMockPlugin from '@line/liff-mock';

liff.use(new LiffMockPlugin());
liff.init({ liffId: '...' }); // Uses mock data, no server calls
```

---

## 4. Pluggable SDK vs LIFF Plugins

These are different concepts:

| | Pluggable SDK | LIFF Plugins |
|---|---|---|
| Purpose | Reduce bundle size by importing only needed APIs | Extend SDK with custom functionality |
| Mechanism | `import X from '@line/liff/module'` + `liff.use(new X())` | Custom class with `name` + `install()` |
| Access | Standard LIFF APIs | Custom namespace: `liff.$[name]` |
| Availability | npm only, SDK v2.22.0+ | CDN or npm, SDK v2.19.0+ |

Both use `liff.use()` but serve different purposes. Pluggable SDK modules activate built-in APIs; LIFF plugins add new ones.

For pluggable SDK module list → see [api.md § Pluggable SDK](api.md).
