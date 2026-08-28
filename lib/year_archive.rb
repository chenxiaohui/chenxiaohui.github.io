module YearArchive
  module_function

  def groups(posts)
    posts.group_by { |post| post.date.year }.sort.reverse.to_h
  end

  def path(year)
    "/archive/#{Integer(year)}/"
  end
end
