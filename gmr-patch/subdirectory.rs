use clap::Parser;
use gmr_cli::cli::Cli;

fn an_initialised_repository() -> tempfile::TempDir {
    let dir = tempfile::tempdir().unwrap();
    std::process::Command::new("git")
        .args(["init", "-q"])
        .current_dir(dir.path())
        .status()
        .expect("git is on PATH in this test environment");
    std::fs::create_dir_all(dir.path().join("repo/src")).unwrap();
    dir
}

async fn gmr(args: &[&str]) -> i32 {
    gmr_cli::run(Cli::parse_from(
        std::iter::once("gmr").chain(args.iter().copied()),
    ))
    .await
    .expect("the verb runs")
}

#[tokio::test]
async fn check_from_a_subdirectory_reads_the_journal_of_the_workspace_above_it() {
    let dir = an_initialised_repository();
    let root = dir.path().to_str().unwrap();
    let sub = dir.path().join("repo/src");

    gmr(&["--repo", root, "init", "--json"]).await;
    assert!(dir.path().join(".anchor").is_dir());

    gmr(&["--repo", sub.to_str().unwrap(), "check", "--json"]).await;

    assert!(
        !dir.path().join("repo/src/.anchor").exists(),
        "a subdirectory has no journal of its own; opening a fresh one there answers \
         `observed 0` for a workspace whose anchors live one level up"
    );
    assert!(!dir.path().join("repo/.anchor").exists());
}

#[tokio::test]
async fn init_in_a_subdirectory_still_creates_the_workspace_where_it_was_asked() {
    let dir = an_initialised_repository();
    let root = dir.path().to_str().unwrap();
    let sub = dir.path().join("repo");

    gmr(&["--repo", root, "init", "--json"]).await;
    gmr(&["--repo", sub.to_str().unwrap(), "init", "--json"]).await;

    assert!(sub.join(".anchor").is_dir(), "init names its own directory");
}

#[test]
fn a_directory_with_no_workspace_above_it_is_its_own_root() {
    let dir = tempfile::tempdir().unwrap();
    let sub = dir.path().join("a/b");
    std::fs::create_dir_all(&sub).unwrap();
    let sub = sub.canonicalize().unwrap();

    assert_eq!(gmr_cli::probes::workspace_root(&sub), sub);
}
