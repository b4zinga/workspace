import json
import sys


def parse_codeql_sarif_json_result(json_file):
    """
    解析codeql sarif v2.1.0版本json格式报告, 并输出命中规则名称及数据流
    """
    if not json_file.endswith(".json"):
        print(f"{json_file} is not a json format file")
        return
    with open(json_file) as f:
        sarif = json.load(f)
    vuln_count = 0
    vuln_type = set()
    for run in sarif.get("runs"):
        results = run.get("results")
        for result in results:
            rule_id = result.get("ruleId")
            vuln_type.add(rule_id)
            if result.get("codeFlows", "") == "":
                print(rule_id)
                for location in result.get("locations"):
                    vuln_count += 1
                    file_path = (
                        location.get("physicalLocation")
                        .get("artifactLocation")
                        .get("uri")
                    )
                    start_line = (
                        location.get("physicalLocation").get("region").get("startLine")
                    )
                    start_column = (
                        location.get("physicalLocation")
                        .get("region")
                        .get("startColumn")
                    )
                    print(f"\t{file_path}#L{start_line}-C{start_column}")
            else:
                for code_flow in result.get("codeFlows"):
                    print(rule_id)
                    vuln_count += 1
                    for thread_flow in code_flow.get("threadFlows"):
                        for location in thread_flow.get("locations"):
                            file_path = (
                                location.get("location")
                                .get("physicalLocation")
                                .get("artifactLocation")
                                .get("uri")
                            )
                            start_line = (
                                location.get("location")
                                .get("physicalLocation")
                                .get("region")
                                .get("startLine")
                            )
                            start_column = (
                                location.get("location")
                                .get("physicalLocation")
                                .get("region")
                                .get("startColumn")
                            )
                            message = (
                                location.get("location").get("message").get("text")
                            )
                            print(
                                f"\t{file_path}#L{start_line}-C{start_column}:{message}"
                            )
    # print(f"vulnerability type: {vuln_type}")
    print(f"Total {len(vuln_type)} types of vulnerabilities")
    print(f"Total {vuln_count} vulnerabilities")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage\n\tpython {sys.argv[0]} [json_file]")
        sys.exit()
    else:
        json_file = sys.argv[1]
        parse_codeql_sarif_json_result(json_file)
