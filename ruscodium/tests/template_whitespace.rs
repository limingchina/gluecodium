use ruscodium::template::render;
use serde_json::json;
use std::{
    fs,
    sync::atomic::{AtomicUsize, Ordering},
};

static SEQUENCE: AtomicUsize = AtomicUsize::new(0);

// Expected bytes were measured using Gluecodium's configured Trimou engine.
fn render_template(template: &str, partial: Option<&str>) -> String {
    let dir = std::env::temp_dir().join(format!(
        "ruscodium-whitespace-{}-{}",
        std::process::id(),
        SEQUENCE.fetch_add(1, Ordering::Relaxed)
    ));
    fs::create_dir_all(&dir).unwrap();
    fs::write(dir.join("main.mustache"), template).unwrap();
    if let Some(value) = partial {
        fs::write(dir.join("part.mustache"), value).unwrap();
    }
    let result = render(
        &dir,
        &json!({
            "schema": "gluecodium.template.render-request", "version": 1,
            "template": "main", "data": {"one": true, "no": false, "name": "outer"}
        }),
    )
    .unwrap();
    fs::remove_dir_all(dir).unwrap();
    result
}

#[test]
fn multiline_comments_and_standalone_sections_match_trimou() {
    for (template, expected) in [
        ("{{#one}}{{!!\n}}\nX{{/one}}", "X"),
        ("{{#one}} {{!!\n}} \nX\n{{/one}}", "X\n"),
        ("{{#one}}{{!!\n}}\n\nX\n{{/one}}", "\nX\n"),
        ("{{#one}}{{!!\n}}\r\nX\r\n{{/one}}", "X\r\n"),
        ("A{{!!\n}}\nB", "A\nB"),
        ("{{#no}}{{!!\n}}x{{/no}}B", "B"),
        ("{{#one}}{{!!\n}}{{#one}}\nX\n{{/one}}\n{{/one}}", "X\n"),
        ("{{#one}}   {{/one}}  \nX", "X"),
        ("{{#one}}{{!!\n}}{{/one}}", ""),
        ("{{#one}}{{!!\n}}  X{{/one}}", "  X"),
    ] {
        assert_eq!(render_template(template, None), expected, "{template:?}");
    }
}

#[test]
fn inline_definitions_and_nested_partials_match_trimou() {
    for (template, expected) in [
        ("{{+p}}x{{/p}}\nX", "\nX"),
        ("{{+p}}\nx\n{{/p}}\nX", "\nX"),
        ("{{+p}}x{{/p}}\r\nX", "\r\nX"),
        ("{{>p}}\n{{+p}}\nx\n{{/p}}\n", "\nx\n\n"),
        ("{{#no}}\nx\n{{/no}}{{!!\n\n}}{{+p}}\nx\n{{/p}}\nY", "Y"),
        (
            "{{#one}}\nx\n{{/one}}{{!!\n\n}}{{+p}}\nx\n{{/p}}\nY",
            "x\nY",
        ),
        ("{{#one}}{{+p}}x{{/p}}\n{{/one}}Y", "Y"),
        ("A{{#one}}{{+p}}x{{/p}}\n{{/one}}Y", "A\nY"),
        ("{{!test}}{{+p}}x{{/p}}\nY", "Y"),
        (
            "{{#no}}\nx\n{{/no}}{{!!\n\n}}{{+p}}\nx\n{{/p}}\nY{{>p}}",
            "Y\nx\n",
        ),
    ] {
        assert_eq!(render_template(template, None), expected, "{template:?}");
    }
    assert_eq!(
        render_template("A\n{{>part}}\nB", Some("{{+p}}\nx\n{{/p}}\n")),
        "A\n\nB"
    );
    for (template, expected) in [
        ("  {{#one}}{{>part}}{{/one}}\nZ", "  x\n  y\nZ"),
        ("  {{!hi}}  {{>part}}\nZ", "  x\n  y\nZ"),
        ("  {{>part}}{{>part}}\nZ", "  x\n  y\nx\ny\nZ"),
        ("  {{#no}}{{>part}}{{/no}}{{>part}}\nZ", "x\ny\nZ"),
    ] {
        assert_eq!(render_template(template, Some("x\ny\n")), expected);
    }
}
