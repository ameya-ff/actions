import re
import os
import sys

def clean_content(content):
    lines = content.splitlines()
    new_lines = []
    
    in_objects = False
    current_object = []
    brace_count = 0
    
    for line in lines:
        if not in_objects:
            if line.strip() == 'objects = {':
                in_objects = True
                new_lines.append(line)
            else:
                if 'shareextension' not in line.lower():
                    new_lines.append(line)
            continue
            
        if line.strip() == '};' and brace_count == 0:
            in_objects = False
            new_lines.append(line)
            continue
            
        current_object.append(line)
        line_no_comments = re.sub(r'/\*.*?\*/', '', line)
        brace_count += line_no_comments.count('{')
        brace_count -= line_no_comments.count('}')
        
        if brace_count == 0:
            object_str = '\n'.join(current_object)
            if 'shareextension' not in object_str.lower():
                filtered_obj_lines = []
                for l in current_object:
                    if 'shareextension' not in l.lower():
                        filtered_obj_lines.append(l)
                new_lines.extend(filtered_obj_lines)
            current_object = []
            
    return '\n'.join(new_lines) + '\n'

def clean_podfile(content):
    lines = content.splitlines()
    new_lines = []
    skip_block = False
    block_depth = 0
    
    for line in lines:
        if not skip_block:
            if "target 'ShareExtension' do" in line:
                skip_block = True
                block_depth = 1
                continue
            if "if Dir.exist?(share_ext_xcconfig_dir)" in line:
                skip_block = True
                block_depth = 1
                continue
            if 'shareextension' in line.lower():
                continue
            new_lines.append(line)
        else:
            tokens = re.findall(r'\bdo\b|\bend\b', line)
            for token in tokens:
                if token == 'do':
                    block_depth += 1
                elif token == 'end':
                    block_depth -= 1
            if block_depth == 0:
                skip_block = False
            continue
            
    return '\n'.join(new_lines) + '\n'

def main():
    print("=== Stripping ShareExtension target for CI build ===")
    
    ios_proj = "ios/Runner.xcodeproj/project.pbxproj"
    macos_proj = "macos/Runner.xcodeproj/project.pbxproj"
    ios_podfile = "ios/Podfile"
    
    if os.path.exists(ios_proj):
        print(f"Cleaning {ios_proj}...")
        with open(ios_proj, 'r') as f:
            content = f.read()
        cleaned = clean_content(content)
        with open(ios_proj, 'w') as f:
            f.write(cleaned)
        print("iOS project cleaned successfully.")
        
    if os.path.exists(macos_proj):
        print(f"Cleaning {macos_proj}...")
        with open(macos_proj, 'r') as f:
            content = f.read()
        cleaned = clean_content(content)
        with open(macos_proj, 'w') as f:
            f.write(cleaned)
        print("macOS project cleaned successfully.")
        
    if os.path.exists(ios_podfile):
        print(f"Cleaning {ios_podfile}...")
        with open(ios_podfile, 'r') as f:
            content = f.read()
        cleaned = clean_podfile(content)
        with open(ios_podfile, 'w') as f:
            f.write(cleaned)
        print("iOS Podfile cleaned successfully.")

if __name__ == '__main__':
    main()
