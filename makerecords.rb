#!/usr/bin/env ruby
require "rubygems"
require "mysql"

# # Create a new file and write to it  
f = File.open('chile1.txt', 'w')
 
f.puts "type\ttime\tcontact\tname\tlocation\ttweet author\ttext\ttime\n"

db = Mysql.new("localhost", "root", "", "haiti_db")

del = db.query("DELETE FROM `tweets` WHERE `text` LIKE '%[nombre]%' OR `text` LIKE '%[localidad]' OR `text` LIKE '%[lista de' OR `text` LIKE '%[Lista de'")

dis = db.query("SELECT DISTINCT text FROM `tweets`")

def parse_type(text)
  if text.downcase =~ /#(need|offer|have|closed|buscapersonas|open|dono|edificiocolapso|taybien|toybien|tavivo|necesidad|necesita|donacion|ofrece|tengo|tenemos|imok|ruok|missing|evac|damage|estasbien|estabien|estoybien|todobien|survivor|sebusca)/
    return $1
  end
  return ""
end

def parse_contact(text)
  if text.downcase =~ /(\#contacto|\#contact|\#contactar|\#con |\#cont |\#avisar|\#telefono|\#fono|\#tel|\#cel)([^#]*)/
    return $2
  end
  return ""
end

def parse_location(text)
  if text.downcase =~ /(#sitio|\#location|\#en |\#loc |\#zona|\#localidad|\#gps|\#lugar)([^#]*)/
    loc = $2
    if loc.length < 2
       if text.downcase =~ /(#sitio|\#location|\#en|\#loc|\#gps|\#localidad|\#zona|\#lugar) #([^#]*)/
         loc = $2
       end
    end
    return loc
  end
  return ""
end

def parse_info(text)
  if text.downcase =~ /(#info)([^#]*)/
    return $2
  end
  return ""
end

def parse_type_s(text)
  if text.downcase =~ /\#(need|necesita|offer|have|ofrece|closed|open|ofrece|taybien|dono|edificiocolapso|toybien|tavivo|necesidad|tengo|tenemos|imok|ruok|missing|evac|damage|estasbien|estabien|estoybien|todobien|survivor|sebusca)([^#]*)/
    return $2
  end
  return ""
end

def parse_complete(text)
  if text.downcase =~ /(#encontr|#found)/
    return "1"
  end
  return "0"  
end

def parse_name(text)
  if text.downcase =~ /(#name|#nombre)([^#]*)/
    return $2
  end
  return ""
end

def parse_status(text)
  if text.downcase =~ /(#status|#situaci|#situati)([^#]*)/
    cur = $2
    i = cur.index(" ")
    return cur[i...cur.length] if i != nil && i > 0
    return $2
  end
  return ""
end

list_array = []

dis.each do |group|

  res = db.query("SELECT id, author, text, time FROM tweets WHERE text = '" + group[0] + "'")
  row = res.fetch_row
 
  is_TtT = 0  

  twt1 = row[2].gsub("[", "")
  twt = twt1.gsub("]", "")

  type = parse_type(twt).strip
  contact = parse_contact(twt).strip
  contact.gsub!("...", "")
  contact.strip!
  type_s = parse_type_s(twt).strip
  location = parse_location(twt).strip
  info = parse_info(twt).strip
  info.gsub!("...", "")
  info.strip!
  complete = parse_complete(twt).strip
  name = parse_name(twt).strip
  status = parse_status(twt).strip
  if status != ""
    status[0...3] = ""
  end
  
  if type_s.length < 2
    type_s = name
  end
  
  if contact.length > 3 || location.length > 3 || info.length > 3
    find_record = db.query("SELECT contact, location, info, complete, status FROM records_chile WHERE type = '" + type + "' AND type_specifics = '" + type_s + "'")
    if find_record != nil && (row2 = find_record.fetch_row) != nil
      dirty = 0
         
      if row2[0].index(contact) == nil
        if row2[0].length > 0
            contact = row2[0] + "/" + contact
        end
        dirty = 1
      else
        info = row2[0]
      end
      
      if row2[1].length >= location.length || location.index("http:") != nil
        location = row2[1]
      else
        dirty = 1
      end
      
      if row2[2].index(info) == nil
        if row2[2].length > 0
            info = row2[2] + "/" + info
        end
        dirty = 1
      else
        info = row2[2]
      end
      
      if row2[4] && row2[4].length >= status.length
        status = row2[4]
      else
        dirty = 1
      end    
      
      if row2[3] != complete
        dirty = 1
      end
      
      if dirty == 1
        db.query("UPDATE records_chile SET contact = '" + contact + "', location = '" + location + "', info = '" + info +
               "', complete = '" + complete + "', status = '" + status + "' WHERE type = '" + type + "' AND type_specifics = '" + type_s + "'")
      end
    else
      db.query("INSERT INTO records_chile (type, type_specifics, location, info, contact, TtT, time, complete) VALUES ('" + type + "', '" +
              type_s + "', '" + location + "', '" + info +"', '" + contact + "', '1', '" + row[3] + "', '" + complete + "')")
    end
  end
  
end






